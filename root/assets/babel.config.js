module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: '> 0.25%, not dead',
        modules: false
      },
    ],
    "@babel/preset-typescript"
  ],
  plugins: [
    '@babel/plugin-proposal-optional-chaining',
    '@babel/plugin-proposal-decorators',
    "@babel/syntax-dynamic-import"
  ],
};
