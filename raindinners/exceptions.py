class RainDinnersInterfaceError(Exception):
    ...


class DecodeError(RainDinnersInterfaceError):
    ...


class RainDinnersAPIError(RainDinnersInterfaceError):
    ...


class RainDinnersNetworkError(RainDinnersAPIError):
    ...
