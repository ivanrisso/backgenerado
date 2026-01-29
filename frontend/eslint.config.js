import antfu from '@antfu/eslint-config'

export default antfu({
    vue: true,
    typescript: true,
    formatters: true,
    stylistic: false,
    jsonc: false,
    yaml: false,
    rules: {
        'no-console': 'warn',
        'vue/multi-word-component-names': 'off',
        'perfectionist/sort-imports': 'off',
        'perfectionist/sort-named-imports': 'off',
        'perfectionist/sort-exports': 'off',
        'ts/no-empty-object-type': 'off',
        'style/indent': 'off',
        'style/eol-last': 'off',
        'unused-imports/no-unused-vars': 'off',
        'no-alert': 'off',
        'ts/no-use-before-define': 'off',
        'vue/valid-v-slot': 'off',
        'vue/custom-event-name-casing': 'off',
        'unicorn/prefer-number-properties': 'off'
    }
})
