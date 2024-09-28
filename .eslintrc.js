module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    "vuetify",
    "@vue/eslint-config-typescript"
  ],
  rules: {
    "vue/multi-word-component-names": "off",
    semi: ["error", "always", { omitLastInOneLineBlock: false }],
    "comma-dangle": ["error", "never"],
    quotes: ["error", "double"],
    "vue/script-indent": [0]
  }
};
