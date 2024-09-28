<script setup lang="ts">
import { BOARD_SIZE } from "@/utils/globals";
import Card from "./Card.vue";
import { Information } from "@/types/information";
import { Hand } from "@/types/hand";

const props = defineProps<{
  information: Information,
  cards: Hand,
  userID?: string,
}>();

const gameCards = computed(() => {
  const newCards = [];
  for (let index = 0; index < BOARD_SIZE; index++) {
    if (index > props.information.poker_cards.board.length - 1) {
      newCards.push({ string: "B" });
    } else {
      newCards.push(props.information.poker_cards.board[index]);
    }
  }
  return { board: newCards };
});

const players = computed(() => {
  const players = [];
  for (const player of props.information.players) {
    if (player.id === props.userID) {
      players.push(player);
    }
  }
  for (const player of props.information.players) {
    if (player.id !== props.userID) {
      players.push(player);
    }
  }
  return players;
});

const getPlayerPositionStyle = (index: number) => {
  const positions = [
    {
      bottom: "-10%",
      left: "50%",
      transform: "translateX(-50%)"
    },
    {
      bottom: "0%",
      left: "10%"
    },
    {
      top: "40%",
      left: "-20%",
      transform: "translateY(-50%)"
    },
    {
      top: "-20%",
      left: "10%"
    },
    {
      top: "-20%",
      right: "10%"
    },
    {
      top: "40%",
      right: "-20%",
      transform: "translateY(-50%)"
    },
    {
      bottom: "0%",
      right: "10%"
    }
  ];

  return positions[index];
};
</script>

<template>
  <div class="base">
    <div class="board">
      <div class="table">
        <div>
          <div class="cards">
            <div v-for="card in gameCards.board" :key="card.value">
              <Card :card="card.string" />
            </div>
          </div>
          <p>
            <strong>
              Pot: {{ props.information.pot }}
            </strong>
          </p>
        </div>
        <div class="players">
          <div
            v-for="(player, index) in players"
            :key="player.id"
            class="player"
            :style="getPlayerPositionStyle(index)"
          >
            <Player
              :back="props.cards && player.id === props.userID ? props.cards?.hand.back.string : 'B'"
              :behind="player.behind"
              :front="props.cards && player.id === props.userID ? props.cards?.hand.front.string : 'B'"
              :position="index"
              :round_bet="player.round_bet"
              :state="player.state"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.base {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.board {
  display: flex;
  flex-direction: row;
  position: relative;
}

.cards {
  display: flex;
  flex-direction: row;
  justify-content: center; /* Центрирование по горизонтали */
  gap: 1px;
  width: 192px; /* Убедитесь, что ширина занимает всю доступную область */
  position: absolute; /* Позволяет централизовать карты */
  top: 50%; /* Позиционируем по вертикали */
  left: 50%; /* Позиционируем по горизонтали */
  transform: translate(-50%, -50%); /* Центрируем по обеим осям */
}

.table {
  position: relative;
  width: 400px; /* Ширина эллипса */
  height: 300px; /* Высота эллипса */
  border: 2px solid #000; /* Граница эллипса */
  border-radius: 50%; /* Создает эллипс */
}

.player {
  position: absolute;
  width: 64px;
  height: 32px;
}
</style>
