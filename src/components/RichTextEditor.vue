<template>
  <div class="rich-text-editor-wrapper">
    <div class="editor-toolbar">
      <button
        v-for="tool in toolbarButtons"
        :key="tool.id"
        :title="tool.label"
        class="toolbar-btn"
        @click="execCommand(tool.command, tool.value)"
        :class="{ active: isCommandActive(tool.command) }"
      >
        {{ tool.icon }}
      </button>
      
      <!-- Image upload button -->
      <button
        title="درج تصویر"
        class="toolbar-btn"
        @click="triggerImageUpload"
      >
        🖼️
      </button>
      
      <input
        ref="imageInput"
        type="file"
        accept="image/*"
        style="display: none"
        @change="insertImage"
      >

      <!-- Color picker -->
      <div class="color-picker-wrapper">
        <label title="رنگ متن">
          <span class="toolbar-btn-text">🎨</span>
          <input
            type="color"
            @change="changeTextColor"
            value="#000000"
            style="cursor: pointer;"
          >
        </label>
      </div>

      <!-- Clear formatting -->
      <button
        title="پاک کردن فرمت بندی"
        class="toolbar-btn"
        @click="clearFormatting"
      >
        ✖️
      </button>
    </div>

    <div
      ref="editor"
      class="editor-content"
      contenteditable="true"
      @input="handleInput"
      @paste="handlePaste"
    ></div>

    <div class="editor-stats">
      {{ characterCount }} کاراکتر | {{ wordCount }} کلمه
    </div>
  </div>
</template>

<script>
export default {
  name: 'RichTextEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'متن خود را اینجا وارد کنید...'
    }
  },
  data() {
    return {
      characterCount: 0,
      wordCount: 0,
      toolbarButtons: [
        { id: 'bold', icon: '𝗕', command: 'bold', label: 'متن درشت' },
        { id: 'italic', icon: '𝘐', command: 'italic', label: 'متن کج' },
        { id: 'underline', icon: 'U̲', command: 'underline', label: 'خط زیر' },
        { id: 'strikethrough', icon: 'S̶', command: 'strikeThrough', label: 'خط خورده' },
        { id: 'separator1', icon: '|', command: null, label: '' },
        { id: 'h1', icon: 'H1', command: 'formatBlock', value: 'h1', label: 'عنوان 1' },
        { id: 'h2', icon: 'H2', command: 'formatBlock', value: 'h2', label: 'عنوان 2' },
        { id: 'h3', icon: 'H3', command: 'formatBlock', value: 'h3', label: 'عنوان 3' },
        { id: 'h4', icon: 'H4', command: 'formatBlock', value: 'h4', label: 'عنوان 4' },
        { id: 'p', icon: 'P', command: 'formatBlock', value: 'p', label: 'پاراگراف' },
        { id: 'separator2', icon: '|', command: null, label: '' },
        { id: 'unordered-list', icon: '• ', command: 'insertUnorderedList', label: 'لیست نقطه‌ای' },
        { id: 'ordered-list', icon: '1.', command: 'insertOrderedList', label: 'لیست شماره‌ای' },
        { id: 'blockquote', icon: '"', command: 'formatBlock', value: 'blockquote', label: 'نقل قول' },
        { id: 'separator3', icon: '|', command: null, label: '' },
        { id: 'left', icon: '⬅', command: 'justifyLeft', label: 'چپ‌چین' },
        { id: 'center', icon: '⬍', command: 'justifyCenter', label: 'وسط‌چین' },
        { id: 'right', icon: '➡', command: 'justifyRight', label: 'راست‌چین' },
        { id: 'separator4', icon: '|', command: null, label: '' },
        { id: 'link', icon: '🔗', command: 'createLink', label: 'لینک' },
        { id: 'hr', icon: '─', command: 'insertHorizontalRule', label: 'خط افقی' }
      ]
    }
  },
  mounted() {
    this.$refs.editor.innerHTML = this.modelValue;
    if (!this.modelValue) {
      this.$refs.editor.setAttribute('data-placeholder', this.placeholder);
    }
    this.updateStats();
  },
  methods: {
    execCommand(command, value = null) {
      if (!command) return;
      
      if (command === 'createLink') {
        const url = prompt('لینک را وارد کنید:', 'https://');
        if (url) {
          document.execCommand(command, false, url);
        }
      } else if (value) {
        document.execCommand(command, false, value);
      } else {
        document.execCommand(command, false, null);
      }
      
      this.$refs.editor.focus();
    },
    isCommandActive(command) {
      return document.queryCommandState(command);
    },
    handleInput() {
      const html = this.$refs.editor.innerHTML;
      this.$emit('update:modelValue', html);
      this.updateStats();
    },
    handlePaste(event) {
      // Allow paste with formatting
      event.preventDefault();
      const text = event.clipboardData.getData('text/html') || event.clipboardData.getData('text/plain');
      document.execCommand('insertHTML', false, text);
    },
    triggerImageUpload() {
      this.$refs.imageInput.click();
    },
    insertImage(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        img.style.cursor = 'pointer';
        img.title = 'کلیک برای حذف تصویر';
        img.onclick = function() {
          if (confirm('آیا مطمئن هستید؟')) {
            this.remove();
          }
        };
        
        this.$refs.editor.focus();
        document.execCommand('insertHTML', false, img.outerHTML);
        this.$emit('update:modelValue', this.$refs.editor.innerHTML);
        this.updateStats();
      };
      reader.readAsDataURL(file);

      // Reset input
      event.target.value = '';
    },
    changeTextColor(event) {
      document.execCommand('foreColor', false, event.target.value);
      this.$refs.editor.focus();
    },
    clearFormatting() {
      const text = this.$refs.editor.innerText;
      this.$refs.editor.innerHTML = text;
      this.$emit('update:modelValue', text);
    },
    updateStats() {
      const text = this.$refs.editor.innerText;
      this.characterCount = text.length;
      this.wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    }
  }
}
</script>

<style scoped>
.rich-text-editor-wrapper {
  border: 2px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  background: white;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  padding: 10px;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  direction: rtl;
}

.toolbar-btn {
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
  min-width: 32px;
  text-align: center;
  font-weight: bold;
}

.toolbar-btn:hover {
  background: #e8f4f8;
  border-color: #0099FF;
}

.toolbar-btn.active {
  background: #0099FF;
  color: white;
  border-color: #0099FF;
}

.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toolbar-btn-text {
  display: inline-block;
  font-size: 16px;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
}

.color-picker-wrapper label {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.color-picker-wrapper input[type="color"] {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.editor-content {
  min-height: 300px;
  padding: 15px;
  outline: none;
  direction: rtl;
  text-align: right;
  line-height: 1.6;
  font-family: inherit;
  font-size: 14px;
  color: #333;
}

.editor-content[data-placeholder]:empty:before {
  content: attr(data-placeholder);
  color: #999;
  font-style: italic;
}

.editor-content img {
  margin: 10px 0;
  border-radius: 4px;
  border: 1px solid #ddd;
  padding: 5px;
  transition: all 0.3s ease;
}

.editor-content img:hover {
  border-color: #0099FF;
  box-shadow: 0 0 8px rgba(0, 153, 255, 0.2);
}

.editor-content h1,
.editor-content h2,
.editor-content h3,
.editor-content h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: bold;
  color: #1a1a1a;
}

.editor-content h1 {
  font-size: 28px;
}

.editor-content h2 {
  font-size: 24px;
}

.editor-content h3 {
  font-size: 20px;
}

.editor-content h4 {
  font-size: 18px;
}

.editor-content blockquote {
  border-right: 4px solid #0099FF;
  background: #f0f7ff;
  margin: 10px 0;
  padding: 15px;
  border-radius: 4px;
  color: #555;
  font-style: italic;
}

.editor-content ul,
.editor-content ol {
  margin: 10px 0;
  padding-right: 25px;
}

.editor-content li {
  margin: 5px 0;
}

.editor-stats {
  background: #f0f0f0;
  padding: 8px 15px;
  font-size: 12px;
  color: #666;
  border-top: 1px solid #e0e0e0;
  text-align: left;
}
</style>
