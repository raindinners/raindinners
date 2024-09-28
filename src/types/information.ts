import { Round } from "../enums/round.ts";
import { Position } from "../enums/position.ts";
import { Cards } from "./cards.ts";
import { Traits } from "./traits.ts";
import { Player } from "./player.ts";
import { PlayerAction } from "./playerAction.ts";

export type Information = {
    traits: Traits,
    round: Round,
    players: Player[],
    current: Position,
    poker_cards: Cards,
    flop_dealt: boolean,
    pot: bigint,
    pot_rake: bigint,
    auto: PlayerAction,
    time: number | null | undefined,
    actions: PlayerAction[] | null | undefined,
}
