<script setup lang="ts">
import { useRouter } from "vue-router";
import { useWebSocket } from "@vueuse/core";
import { AutoEvent } from "@/enums/autoEvent";
import { StartState } from "@/enums/startState";
import { EventType } from "@/enums/eventType";
import {Service} from "@/enums/service";

const router = useRouter();

const tab = ref("home");
const service = ref(tab.value);

const userID = ref(router.currentRoute.value.query.userID);

const pokerIsJoined = ref(false);
const pokerCards = ref(null);
const pokerIsStarted = ref<boolean>(false);
const pokerStartTimerID = ref<number>(0);
const poker = ref(router.currentRoute.value.query.poker);
const pokerInformation = ref(null);

const log = ref<{ title: string, text: string }[]>([]);

const showAlert = ref(false);
const alertText = ref(null);

watch(tab, () => {
  service.value = tab.value.toUpperCase();
});
provide("showAlert", showAlert);
provide("poker", poker);
const { send } = useWebSocket(
  `${import.meta.env.VITE_WEBSOCKET_URL}/${userID.value}`, {
    onMessage (_, message) {
        const response = JSON.parse(message.data);

        if (response.service === Service.POKER) {
            if (response.event_type in AutoEvent) {
                switch (response.event_type) {
                    case AutoEvent.INFORMATION: {
                        pokerInformation.value = response.result;
                        if (!pokerCards.value) {
                            getCards();
                        }
                    }
                        return;
                    case AutoEvent.LOG: {
                        log.value.push({title: "Information", text: response.result});
                    }
                        return;
                    case AutoEvent.START: {
                        switch (response.result.state) {
                            case StartState.STARTING: {
                                pokerStartTimerID.value = setTimeout(() => {
                                        pokerIsStarted.value = true;
                                    },
                                    response.result.time);
                            }
                                return;
                            case StartState.STARTED: {
                                clearTimeout(pokerStartTimerID.value);
                                pokerIsStarted.value = true;
                            }
                                return;
                            case StartState.STOPPED: {
                                clearTimeout(pokerStartTimerID.value);
                                pokerIsStarted.value = false;
                                pokerInformation.value = null;
                            }
                                return;
                        }
                    }
                        return;
                    case AutoEvent.WINNERS: {
                        pokerCards.value = null;
                        pokerInformation.value.current = null;
                    }
                }
            } else if (response.event_type in EventType) {
                switch (response.event_type) {
                    case EventType.EXECUTE_ACTION: {
                        if (!response.result) {
                            showMessage("Execute action failed")
                        }
                    }
                        return;
                    case EventType.EXIT: {
                        if (response.result.id === userID.value) {
                            pokerCards.value = null;
                            pokerIsJoined.value = false;
                            pokerIsStarted.value = false;
                            pokerInformation.value = null;
                        }

                        log.value.push({title: "Poker", text: `Player #${response.result.id} left!`});
                    }
                        return;
                    case EventType.GET_CARDS: {
                        pokerCards.value = response.result;
                    }
                        return;
                    case EventType.JOIN: {
                        if (response.result.id === userID.value) {
                            pokerIsJoined.value = true;
                        }
                        log.value.push({title: "Poker", text: `Player #${response.result.id} joined!`});
                    }
                }
            } else {
                log.value.push({title: "Error", text: "Error was occurred"});
            }
        } else {
            log.value.push({title: "Error", text: "Error was occurred"});
        }
    }
  }
);

const executeAction = (action: bigint, amount: bigint, position: bigint) => {
  send(
    JSON.stringify(
      {
          service: service.value,
        type: EventType.EXECUTE_ACTION,
        request: {
          poker: poker.value,
          action: {
            action,
            amount,
            position
          }
        }
      }
    )
  );
};
const exit = () => {
  send(
    JSON.stringify(
      {
          service: service.value,
        type: EventType.EXIT,
        request: {
          poker: poker.value
        }
      }
    )
  );
};
const getCards = () => {
  send(
    JSON.stringify(
      {
          service: service.value,
        type: EventType.GET_CARDS,
        request: {
          poker: poker.value
        }
      }
    )
  );
};
const join = () => {
  console.log(service.value);
    send(
    JSON.stringify(
      {
          service: service.value,
        type: EventType.JOIN,
        request: {
          poker: poker.value
        }
      }
    )
  );
};

const showMessage = text => {
    showAlert.value = true;
    alertText.value = text;
}
const showPlayer = player => {
  showAlert.value = true;
  alertText.value = `Player #${player.id}: stack ${player.stack}, round bet ${player.round_bet}`;
};
</script>

<template>
  <v-card class="fullScreen">
    <v-tabs
      v-model="tab"
      bg-color="primary"
    >
      <v-tab color="black" value="home">Home</v-tab>
        <v-tab color="black" value="chat">Chat</v-tab>
      <v-tab color="black" value="poker">Poker</v-tab>
        <v-tab color="black" value="settings">Settings</v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="home">
          <div>
            <h1>Welcome to RainDinners</h1>
            <p>You can connect to any games via my Telegram-Bot!</p>
          </div>
        </v-tabs-window-item>
          <v-tabs-window-item value="chat">
              <div>
                  <h2>Information messages will be appeared here</h2>
                  <Chat :log="log"/>
              </div>
          </v-tabs-window-item>
        <v-tabs-window-item value="poker">
          <div v-if="pokerInformation">
            <Alert :text="alertText" />
            <Table
              v-if="pokerCards"
              :cards="pokerCards"
              :information="pokerInformation"
              :user-i-d="userID"
              @show-player="showPlayer"
            />
            <Actions
              v-if="pokerInformation?.players[pokerInformation?.current].id === userID"
              :information="pokerInformation"
              @execute-action="executeAction"
            />
          </div>
          <div v-else-if="!pokerIsJoined" class="centered">
            <InputText
              id="poker"
              label="Type and join!"
              :model-value="poker"
              placeholder="Enter room"
              provide-key="poker"
            />
            <VBtn
              v-if="poker"
              @click="join()"
            >
              Join
            </VBtn>
          </div>
          <div v-else class="centered">
            <h2>Loading...</h2>
            <VBtn @click="exit()">Exit</VBtn>
          </div>
        </v-tabs-window-item>
          <v-tabs-window-item value="settings">
              <div class="centered">
                  <VBtn @click="exit()">Exit</VBtn>
              </div>
          </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.fullScreen {
  height: 100vh;
  position: relative;
}

.centered {
  display: flex;
  flex-direction: column;
  place-items: center;
}
</style>
