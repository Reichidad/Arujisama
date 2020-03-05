<template>
  <div class="delete-memo">
    <div class="memoClass koreanFont">
      <h1>정말 삭제하시겠어요?</h1>
      <p style="white-space: normal">{{ memo }}</p>
      <p>찍은 시간 : {{ convert_time }}</p>
      <div>
        <button class="close-button koreanFont" @click="DeleteStamp">삭제해줘</button>&nbsp;
        <button class="close-button koreanFont" @click="Cancel">안 돼</button>
      </div>
    </div>
  </div>
</template>

<script>
import dateFormat from "dateformat";
import axios from "axios";

export default {
  name: "DeleteStamp",
  props: ["memo", "submit_time", "idx", "parent"],
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
    DeleteStamp: function() {
      var vm = this;
      console.log("스탬프 삭제 시도");
      axios
        .get("/deletestamp", {
          params: {
            stamp_idx: vm.idx
          }
        })
        .then(function(response) {
          console.log(response);
          if (response.data.code == 18) {
            console.log("스탬프 삭제 완료");
            vm.parent.handleUpdate(true);
          }
          else {
            vm.parent.handleUpdate(false);
          }
          vm.$emit("close");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    Cancel: function() {
      this.parent.handleUpdate(false);
      this.$emit("close");
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