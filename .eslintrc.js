module.exports = {
  env: {
    browser: true,
    es2021: true,
    'jest/globals': true,
  },
  extends: [
    'plugin:react/recommended',
    'airbnb',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
    'react-hooks',
    '@typescript-eslint',
    'jest',
  ],
  rules: {
    'no-use-before-define': 'off',
    '@typescript-eslint/no-use-before-define': ['error'],
    'no-underscore-dangle': 0,
    'import/extensions': 'off',
    'import/no-extraneous-dependencies': 'off',
    'import/no-unresolved': 'off',
    'import/prefer-default-export': 'off',
    'import/no-named-as-default': 'off',
    'no-class-assign': 'off',
    'react/prop-types': 'off',
    'react/prefer-stateless-function': [0, { ignorePureComponents: true }],
    'react/jsx-filename-extension': [1, { extensions: ['.js', '.jsx', '.ts', '.tsx'] }],
    'max-len': [0, { code: 200 }],
    'react/jsx-max-props-per-line': [0, { maximum: 3, when: 'always' }],
    'react/jsx-one-expression-per-line': 0,
    'jsx-a11y/no-static-element-interactions': 0,
    'jsx-a11y/click-events-have-key-events': 0,
    'jsx-a11y/label-has-associated-control': 0,
    'jsx-a11y/no-noninteractive-element-interactions': 0,
    'jsx-a11y/label-has-for': 0,
    'react/button-has-type': 0,
    'react/self-closing-comp': 0,
    'react/no-array-index-key': 0,
    'react/forbid-prop-types': 0,
    'react/jsx-props-no-spreading': 0,
    'react/state-in-constructor': 'off',
    'no-else-return': 0,
    'no-shadow': 0,
    'react-hooks/rules-of-hooks': 'error', // Checks rules of Hooks
    'react-hooks/exhaustive-deps': 'warn', // Checks effect dependencies
    indent: [
      'error',
      2,
      {
        SwitchCase: 1,
      },
    ],
    quotes: [
      'error',
      'single',
    ],
    semi: [
      'error',
      'always',
    ],
    'comma-dangle': [1, 'always-multiline'],
    'function-paren-newline': 'off',
  },
  overrides: [
    {
      files: [
        '**/*.stories.*',
      ],
      rules: {
        'import/no-anonymous-default-export': 'off',
        'no-console': 'off',
      },
    },
    {
      files: [
        '**/*.test.tsx',
      ],
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
      },
    },
  ],
};
