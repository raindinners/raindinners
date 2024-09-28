import { Balance } from "./balance.ts";

export type User = {
    id: bigint,
    balance: Balance | null | undefined
}
