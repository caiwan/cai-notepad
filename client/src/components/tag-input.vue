<template>
  <ul
    class="tags"
    :class="{conflict: conflict, empty: pTags.length, disabled: disabled}"
    @click="focusInput"
  >
    <li
      class="tag"
      v-for="tag of pTags"
      :key="tag"
      @click="remove($event, tag)"
    >
      {{ tag }}
    </li>

    <li class="tag-input">
      <input
        ref="tagInput"
        v-model="currentTag"
        @keydown="keydown"
        @input="input"
        @blur="add"
        :disabled="disabled"
      >
      <ul
        v-if="choiceListVisible"
        ref="choiceList"
        :class="{dropup: dropup}"
      >
        <li
          ref="choices"
          v-for="(tag, index) of pChoices"
          :key="index"
          :class="{'tag-choice-selected': index === selectedIndex}"
          @mousedown="deferBlur = true"
          @mouseup="add($event, tag)"
          @mouseover="selectedIndex = index"
        >
          {{ tag }}
        </li>
      </ul>
    </li>

  </ul>
</template>

<script>
let UNDEFINED = -1;
// TODO: Make these configurable in props
let CHOICE_WHITELIST = new Set(['Backspace', 'Delete']);

export default {
  props: {
    tags: {
      type: Array,
      required: false,
      'default': () => []
    },
    choices: {
      type: [Function, Array],
      required: false,
      'default': () => []
    },
    delimiters: {
      type: Array,
      required: false,
      'default': () => ['Tab', 'Enter']
    },
    disabled: {
      type: Boolean,
      required: false,
      'default': () => false
    }
  },
  data: function () {
    return {
      pDelimiters: new Set(this.delimiters),

      pTags: this.tags,
      currentTag: '',
      conflict: false,

      pChoices: this.choices,
      choiceListVisible: false,
      dropup: false,
      selectedIndex: UNDEFINED,

      pressedKey: null,

      deferBlur: false
    };
  },
  methods: {
    keydown(e) {
      this.pressedKey = e.key;

      if (e.key === 'Backspace') {
        if (!this.currentTag) {
          e.preventDefault();
          this.currentTag = this.pTags.pop();
          this.conflict = false;
        }
      }
      else if (this.pDelimiters.has(e.key)) {
        e.preventDefault();

        this.choiceListVisible = false;

        if (this.currentTag && this.currentTag.length > 0) {
          this.add();
          this.focusInput();
        }
        else {
          this.$emit('blur');
        }
      }

      if (this.choiceListVisible) {
        let key = e.key;
        if (this.dropup) {
          if (key === 'ArrowDown') {
            key = 'ArrowUp';
          }
          else if (key === 'ArrowUp') {
            key = 'ArrowDown';
          }
        }

        if (key === 'ArrowDown') {
          e.preventDefault();

          this.selectedIndex = (this.selectedIndex + 1) % this.pChoices.length;
          this.currentTag = this.pChoices[this.selectedIndex];

          this.$nextTick(() => {
            let target = this.$refs.choices[this.selectedIndex];
            let choiceList = this.$refs.choiceList;
            let visibleHeight = choiceList.getBoundingClientRect().height;
            let scrollTop;

            if (this.dropup) {
              let invisibleHeight = choiceList.scrollHeight - visibleHeight;

              scrollTop = invisibleHeight + target.offsetTop;

              if (!(scrollTop > choiceList.scrollTop && scrollTop < choiceList.scrollTop + visibleHeight)) {
                choiceList.scrollTop = scrollTop;
              }
            }
            else {
              let targetHeight = target.getBoundingClientRect().height;
              scrollTop = target.offsetTop + targetHeight;

              if (scrollTop < choiceList.scrollTop) {
                choiceList.scrollTop = scrollTop - targetHeight;
              }
              else if (scrollTop > choiceList.scrollTop + visibleHeight) {
                choiceList.scrollTop = scrollTop - visibleHeight + 2;
              }
            }
          });
        }
        else if (key === 'ArrowUp') {
          e.preventDefault();

          let n = this.pChoices.length;
          this.selectedIndex = ((Math.max(-1, this.selectedIndex - 1) % n) + n) % n;
          this.currentTag = this.pChoices[this.selectedIndex];

          this.$nextTick(() => {
            let target = this.$refs.choices[this.selectedIndex];
            let targetHeight = target.getBoundingClientRect().height;
            let choiceList = this.$refs.choiceList;
            let visibleHeight = choiceList.getBoundingClientRect().height;
            let scrollTop;

            if (this.dropup) {
              let invisibleHeight = choiceList.scrollHeight - visibleHeight;

              scrollTop = invisibleHeight + target.offsetTop + targetHeight;

              if (scrollTop < choiceList.scrollTop) {
                choiceList.scrollTop = scrollTop - targetHeight;
              }
              else if (scrollTop > choiceList.scrollTop + visibleHeight) {
                choiceList.scrollTop = scrollTop - visibleHeight + 5;
              }
            }
            else {
              scrollTop = target.offsetTop;

              if (!(scrollTop > choiceList.scrollTop && scrollTop < choiceList.scrollTop + visibleHeight)) {
                choiceList.scrollTop = scrollTop;
              }
            }
          });
        }
        else if (e.key.length === 1 || CHOICE_WHITELIST.has(e.key)) {
          this.resolveRequired = true;
        }
      }
      else {
        this.resolveRequired = true;
      }
    },
    input(e) {
      this.resolveRequired = true;
    },
    add(e, tag) {
      if (tag) {
        this.currentTag = tag;
        this.deferBlur = false;
      }
      if (!this.deferBlur) {
        this.conflict = false;
        this.choiceListVisible = false;

        if (this.currentTag && this.currentTag.length > 0) {
          let tag = this.currentTag.trim();
          if (tag.length > 0) {
            if (this.pTags.indexOf(tag) === UNDEFINED) {
              this.pTags.push(tag);
              this.currentTag = '';
              this.focusInput();
            }
            else {
              this.conflict = true;
            }
          }
        }
      }

      this.deferBlur = false;
    },
    remove(e, tag) {
      if (this.disabled) {
        return;
      }

      e.stopPropagation();

      this.pTags.splice(this.pTags.indexOf(tag), 1);
      this.conflict = false;
    },
    focusInput() {
      let tagInput = this.$refs.tagInput;
      console.log('loller, focus', { tagInput });
      if (tagInput) {
        tagInput.focus();
      }
    },
    resolveChoices() {
      let choices;

      try {
        choices = this.choices(this.currentTag);
      }
      catch (e) {
        return;
      }

      if (this.choices) {
        Promise.resolve(choices)
          .then(value => {
            this.pChoices = value;
            this.selectedIndex = UNDEFINED;
            this.choiceListVisible = this.pChoices.length > 0;

            this.dropup = this.$refs.tagInput.getBoundingClientRect().top / window.innerHeight >= 0.4;
          });
      }
    }
  },
  created() {
    this.resolveRequired = false;
    this.$nextTick(() => {
      let tagInput = this.$refs.tagInput;
      tagInput.style.width = '2px';
      tagInput.style.width = `${tagInput.scrollWidth + 2}px`
    });
  },
  updated() {
    let tagInput = this.$refs.tagInput;

    if (tagInput) {
      tagInput.style.width = '2px';
      tagInput.style.width = `${tagInput.scrollWidth + 2}px`
    }

    if (this.resolveRequired) {
      this.resolveChoices();
      this.resolveRequired = false;
    }
  }
}
</script>

<style lang="scss" rel="stylesheet/scss">
@import "../scss/_tag-input.scss";
</style>
