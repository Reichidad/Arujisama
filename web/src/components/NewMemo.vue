<template>
  <div>
    <div class="memoClass">
      <h1 class="koreanFont memoFontSize">메모를 입력!</h1>
      <h1 class="koreanFont memoFontSize">메모는 최대 100글자까지 입력이 가능합니다.</h1>
      <p>
        <textarea cols="25" class="new-memo textStyle" v-model="new_stamp_memo" @keydown="MemoLimit"/>
      </p>
      <p>
        <button class="new-memo koreanFont buttonFontSize" type="button" v-on:click="send">메모</button>
        <button
          class="new-memo koreanFont"
          style="margin-left: 15px;"
          type="button"
          @click="$emit('close')"
        >취소</button>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewMemo",
  props: ["memoWrite"],
  data() {
    return {
      new_stamp_memo: ""
    };
  },
  methods: {
    send: function() {
      console.log("send 함수 진입");
      this.memoWrite(this.new_stamp_memo);
      this.$emit("close");
    },
    MemoLimit: function() {
      console.log(this.new_stamp_memo.length);
      if(this.new_stamp_memo.length > 100) {
        this.memoWrite(this.new_stamp_memo);
        this.$emit("close");
      }
    }
  }
};
</script>
<style>
@import url("https://fonts.googleapis.com/css?family=Gloria+Hallelujah&display=swap");
@import url("https://fonts.googleapis.com/css?family=Nanum+Pen+Script&display=swap");
.memoClass {
  width: 600px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.koreanFont {
  font-family: "Nanum Pen Script", cursive;
}
.memoFontSize {
  font-size: 48px;
}
.buttonFontSize {
  font-size: 24px;
}
.textStyle {
  font-size: 16px;
  width: 400px;
  height: 80px;
  text-align: center;
}
</style>