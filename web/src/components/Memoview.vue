<template>
  <div class="memo-view">
    <div class="memoClass koreanFont">
      <h1>스탬프 메모</h1>
      <p style="white-space: normal">{{ memo }}</p>
      <p>찍은 시간 : {{ convert_time }}</p>
      <p></p>
      <!-- 메모 수정기능 미완성
      <div v-if="is_can_edit" class="memo-edit">
        <button class="close-button koreanFont" @click="editmemo">메모수정</button>
        <input class="new-memo" style="font-size: 16px" v-model="new_stamp_memo" />
      </div>
      -->
      <button class="close-button koreanFont" @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script>
import dateFormat from "dateformat";
import axios from "axios";

export default {
  name: "Memoview",
  props: ["memo", "submit_time", "idx", "is_can_edit"],
  data: function() {
    return {
      new_stamp_memo: ""
    };
  },
  computed: {
    convert_time: function() {
      var memo_date = new Date(this.submit_time);
      var now = new Date();
      var timezone = now.getTimezoneOffset();
      memo_date = new Date(Date.parse(memo_date) + timezone * 60 * 1000);
      return dateFormat(memo_date, "yyyy년 m월 d일, H시 M분 s초");
    }
  },
  methods: {
    // TEST용
    editmemo: function() {
      var vm = this;
      console.log("edit 함수 진입");
      console.log(vm.idx);
      axios
        .get("/editstamp", {
          params: {
            stamp_idx: vm.idx,
            edit_memo: vm.new_stamp_memo
          }
        })
        .then(function(response) {
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Gloria+Hallelujah&display=swap");
@import url("https://fonts.googleapis.com/css?family=Nanum+Pen+Script&display=swap");
.koreanFont {
  font-family: "Nanum Pen Script", cursive;
}
</style>