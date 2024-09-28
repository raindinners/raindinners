export function getEnumName (value: any, enum_: any) {
  for (const key in enum_) {
    if (value === enum_[key]) {
      return key.charAt(0).toUpperCase() + key.slice(1).toLowerCase();
    }
  }
}
