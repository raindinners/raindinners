<script setup lang="ts">
import Actions from "@/components/Actions.vue";
import Table from "@/components/Table.vue";
import { useWebSocket } from "@vueuse/core";
import { AutoEvent } from "@/enums/autoEvent";
import { StartState } from "@/enums/startState";
import { EventType } from "@/enums/eventType";
import { useRouter } from "vue-router";

const router = useRouter();

const tab = ref("home");

const isJoined = ref(false);
const userID = ref(router.currentRoute.value.query.userID);
const cards = ref(null);

const isStarted = ref<boolean>(false);
const startTimerID = ref<number>(0);

const poker = ref(router.currentRoute.value.query.poker);
const information = ref(null);

const log = ref<string[]>([]);

const { send } = useWebSocket(
  `ws://31.129.207.46:8080/poker${userID.value}`, {
    onMessage (_, message) {
      const response = JSON.parse(message.data);
      if (response.event_type in AutoEvent) {
        switch (response.event_type) {
          case AutoEvent.INFORMATION: {
            information.value = response.result;
            if (!cards.value) {
              getCards();
            }
          }
            return;
          case AutoEvent.START: {
            switch (response.result.state) {
              case StartState.STARTING: {
                startTimerID.value = setTimeout(() => {
                    isStarted.value = true;
                  },
                  response.result.time);
              }
                return;
              case StartState.STARTED: {
                clearTimeout(startTimerID.value);
                isStarted.value = true;
              }
                return;
              case StartState.STOPPED: {
                clearTimeout(startTimerID.value);
                isStarted.value = false;
                information.value = null;
              }
                return;
            }
          }
            return;
          case AutoEvent.WINNERS: {
            information.value = null;
            for (let index = 0; index < response.result.length; index++) {
              const result = response.result[index];
              let winner = "by all exited";
              let chips;
              if (result instanceof Array) {
                [winner, chips] = result;
              } else {
                chips = result;
              }
              if (chips > 0) {
                winner = "won " + winner;
              } else {
                if (result instanceof Array) {
                  winner = "lose by " + winner;
                } else {
                  winner = "lose by exited";
                }
              }
              log.value.push(`Player #${information.value?.players[index].id} got ${chips} chips and ${winner}`);
            }
          }
        }
      } else if (response.event_type in EventType) {
        switch (response.event_type) {
          case EventType.EXECUTE_ACTION: {
            log.value.push(`Player #${information.value?.players[information.value?.current].id} posted action!`);
          }
            return;
          case EventType.EXIT: {
            log.value.push(`Player #${response.result.id} left!`);
          }
            return;
          case EventType.GET_CARDS: {
            cards.value = response.result;
          }
            return;
          case EventType.JOIN: {
            if (response.result.id === userID.value) {
              isJoined.value = true;
            }
            log.value.push(`Player #${response.result.id} joined!`);
          }
        }
      } else {
        log.value.push("Error was occurred");
      }
    }
  }
);

const executeAction = (action: bigint, amount: bigint, position: bigint) => {
  console.log(action, amount, position);
  send(
    JSON.stringify(
      {
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
        type: EventType.GET_CARDS,
        request: {
          poker: poker.value
        }
      }
    )
  );
};

const join = () => {
  send(
    JSON.stringify(
      {
        type: EventType.JOIN,
        request: {
          poker: poker.value
        }
      }
    )
  );
};
</script>

<template>
  <v-card class="fullScreen">
    <v-tabs
      v-model="tab"
      bg-color="primary"
    >
      <v-tab color="black" value="home">Home</v-tab>
      <v-tab color="black" value="poker">Poker</v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="home">
          <div class="home">
            <h1>Welcome to RainDinners</h1>
            <p>You can connect to any games via my Telegram-Bot!</p>
          </div>
        </v-tabs-window-item>

        <v-tabs-window-item value="poker">
          <div v-if="information">
            <Table
              v-if="cards"
              :cards="cards"
              :information="information"
              :userID="userID"
            />
            <Actions
              v-if="information?.players[information?.current].id === userID"
              :information="information"
              @execute-action="executeAction"
            />
          </div>
          <div v-else-if="!isJoined">
            <InputText
              id="poker"
              v-model="poker"
              label="Type and join!"
              placeholder="Enter room"
              :validation="pokerValidation"
            />
            <VBtn
              v-if="poker"
              @click="join()"
            >
              Join
            </VBtn>
          </div>
          <div v-else>
            <h2>Loading...</h2>
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
</style>
