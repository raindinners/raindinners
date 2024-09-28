export type Balance = {
    id: bigint,
    balance: bigint,
    bonus_increment_time_hours: bigint,
    last_time_claimed_bonus: Date | null | undefined
}
