import { EventType } from "../enums/eventType.ts";

export type Event = {
    type: EventType,
    request: any
}
