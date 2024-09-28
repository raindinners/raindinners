import { AutoEvent } from "../enums/autoEvent.ts";
import { EventType } from "../enums/eventType.ts";

export interface ApplicationResponse<T> {
    ok: boolean
    result: T | null | undefined
    event_type: AutoEvent | EventType | null | undefined
    detail: string | null | undefined
    error: string | null | undefined
    error_code: bigint | null | undefined
}
