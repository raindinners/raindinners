import { Action } from "../enums/action.ts";
import { Position } from "@vueuse/core";

export type PlayerAction = {
  amount: bigint,
  action: Action,
  position: Position
}
