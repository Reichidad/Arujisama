<template>
  <div id="stampBackground">
    <div id="headTitle">ARUJISAMA</div>
    <modals-container />
    <button class="button koreanFont" v-on:click="Logout">로그아웃</button>
    <button class="button koreanFont" v-on:click="DeleteStamp">마지막 스탬프 삭제</button>
    <select class="button koreanFont" v-model="pageSelect">
      <option disabled :value="null">페이지 선택</option>
      <option v-for="page in pages">{{ page }}</option>
    </select>
    <div>
      <div id="tempSpeechBubble">{{ bubbleMsg }}</div>
      <div id="stampBox">
        <div id="stampTitle">{{name}}주인님의 스탬프 카드#{{currentPage}}</div>
        <div class="stampArea">
          <p v-for="stamp in firstLineStamps">
            <template v-if="check(stamp) == 1">
              <button class="stampImage" v-on:click="openExistStamp(stamp)"></button>
            </template>
            <template v-else-if="check(stamp) == 2">
              <button class="nextStampImage" v-on:click="memoWriteRender"></button>
            </template>
            <template v-else>
              <button class="blankImage"></button>
            </template>
          </p>
          <p v-for="stamp in secondLineStamps">
            <template v-if="check(stamp) == 1">
              <button class="stampImage" v-on:click="openExistStamp(stamp)"></button>
            </template>
            <template v-else-if="check(stamp) == 2">
              <button class="nextStampImage" v-on:click="memoWriteRender"></button>
            </template>
            <template v-else>
              <button class="blankImage"></button>
            </template>
          </p>
          <p v-for="stamp in thirdLineStamps">
            <template v-if="check(stamp) == 1">
              <button class="stampImage" v-on:click="openExistStamp(stamp)"></button>
            </template>
            <template v-else-if="check(stamp) == 2">
              <button class="nextStampImage" v-on:click="memoWriteRender"></button>
            </template>
            <template v-else>
              <button class="blankImage"></button>
            </template>
          </p>
        </div>
      </div>
    </div>
    <div id="footer">
      <input
        type="button"
        id="feedbackbutton"
        value="피드백 하러 가기"
        onclick="window.open('https://forms.gle/DEL5EuZU4grkScSx8')"
      />
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import router from "../router";
import axios from "axios";
import NewMemo from "./NewMemo";
import Memoview from "./Memoview";
import DeleteStamp from "./DeleteStamp";
import VModal from "vue-js-modal";
import json from "./message.json";
import format from "string-format";

Vue.use(VModal, { dynamic: true });

export default {
  components: {
    NewMemo
  },
  data() {
    return {
      name: null,
      pages: [],
      currentPage: 1,
      stampNum: 0,
      stamps: null,
      new_stamp_memo: "",
      last_stamp_date: null,
      pageSelect: null,
      bubbleMsg: "",
      kokkoro_comment: json
    };
  },
  created: function() {
    var vm = this;
    axios
      .get("/tokencheck")
      .then(function(response) {
        if (response.status === 200 && response.data.code === 9) {
          console.log("토큰 유효");
          vm.bubbleMsg = vm.kokkoro_comment["GREETING"];
          vm.loadStamp(0);
        } else {
          console.log("토큰 유효하지 않음" + response);
          router.push({ name: "Login" });
        }
      })
      .catch(function(error) {
        console.log(error);
        router.push({ name: "Login" });
      });
  },
  computed: {
    firstLineStamps: function() {
      if (this.stamps == null) {
        return [];
      }
      var arr = [];
      for (var i = 0; i < 5; i++) {
        arr.push({
          exist: this.stamps[i].exist,
          memo: this.stamps[i].memo,
          submit_time: this.stamps[i].submit_time,
          idx: this.stamps[i].idx
        });
      }

      return arr;
    },
    secondLineStamps: function() {
      if (this.stamps == null) {
        return [];
      }
      var arr = [];

      for (var i = 5; i < 10; i++) {
        arr.push({
          exist: this.stamps[i].exist,
          memo: this.stamps[i].memo,
          submit_time: this.stamps[i].submit_time,
          idx: this.stamps[i].idx
        });
      }

      return arr;
    },
    thirdLineStamps: function() {
      if (this.stamps == null) {
        return [];
      }
      var arr = [];

      for (var i = 10; i < 15; i++) {
        arr.push({
          exist: this.stamps[i].exist,
          memo: this.stamps[i].memo,
          submit_time: this.stamps[i].submit_time,
          idx: this.stamps[i].idx
        });
      }

      return arr;
    }
  },
  watch: {
    new_stamp_memo: function() {
      console.log(this.new_stamp_memo + " 변화 감지");
      this.pushNewStamp(this.new_stamp_memo);
    },
    pageSelect: function() {
      console.log(this.pageSelect);
      this.loadStamp(this.pageSelect);
      this.bubbleMsg = format(
        this.kokkoro_comment["PAGE_LOAD"],
        this.pageSelect
      );
    }
  },
  methods: {
    Logout: function() {
      localStorage.clear();
      router.push({ name: "Login" });
    },
    check: function(stamp) {
      // console.log("exist 값 체크:" + stamp.exist);
      return stamp.exist;
    },
    isCanEdit: function(_stamptime) {
      var now = new Date();
      var stamptime_to_date = new Date(_stamptime);
      var reset_time = new Date(this.getResetDate(stamptime_to_date));
      var now_reset_time = new Date(this.getResetDate(now));

      if (now_reset_time.getDate() != reset_time.getDate()) {
        // 날짜가 지난 상태
        return false;
      }
      var stamptime = Date.parse(_stamptime);
      return reset_time > stamptime;
    },
    openExistStamp: function(stamp) {
      console.log(stamp.submit_time);
      var is_can_edit = this.isCanEdit(stamp.submit_time);

      this.$modal.show(Memoview, {
        memo: stamp.memo,
        submit_time: stamp.submit_time,
        idx: stamp.idx,
        modal: this.$modal,
        is_can_edit: is_can_edit
      });
    },
    DeleteStamp: function() {
      var vm = this;
      console.log(this.stampNum);
      if (this.stampNum < 1) {
        this.bubbleMsg = this.kokkoro_comment["EMPTY_STAMP"];
        return;
      } else {
        var stamp = this.stamps[this.stampNum - 1];
        console.log(stamp.submit_time);

        this.$modal.show(DeleteStamp, {
          memo: stamp.memo,
          submit_time: stamp.submit_time,
          idx: stamp.idx,
          parent: this,
          modal: this.$modal
        });
      }
    },
    pushNewStamp: function(new_memo) {
      var vm = this;

      // 스탬프 시간 상관없이 찍고자 할 때는 아래의 if문을 주석 처리. 서버에서도 따로 처리해야함.
      if (!vm.stampTimeCheck(this.last_stamp_date)) {
        vm.bubbleMsg = vm.kokkoro_comment["ALREADY_STAMPED"];
        return;
      }

      if(new_memo.length > 100) {
        console.log(new_memo.length);
        vm.bubbleMsg = vm.kokkoro_comment["MEMO_TOO_BIG"];
        return;
      }

      console.log("새 도장 찍기 시도");
      axios
        .get("/addstamp", {
          params: {
            memo: new_memo
          }
        })
        .then(function(response) {
          if (response.data.code == 16) {
            vm.bubbleMsg = vm.kokkoro_comment["ALREADY_STAMPED"];
            return;
          }
          if (response.data.code == 15) {
            vm.bubbleMsg = vm.kokkoro_comment["STAMP_SUCCESS"];
          }

          if (vm.stampNum == 14) {
            vm.bubbleMsg = vm.kokkoro_comment["FULL_STAMP"];
          }
          vm.loadStamp(0);
          console.log(response);
          console.log("스탬프 갱신완료");
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    memoWriteRender: function() {
      var vm = this;
      this.$modal.show(NewMemo, {
        modal: this.$modal,
        memoWrite: new_memo => {
          vm.new_stamp_memo = new_memo;
        }
      });
    },
    stampTimeCheck: function(_stamptime) {
      // Date 간의 연산은 결과를 초 기준으로 반환한다.
      // ex)
      // var date1 = new Date('7/31/2019')
      // var date2 = new Date('8/1/2019')
      // var result = date2 - date1
      // >> result = 86400000

      console.log("Date 계산 시작");
      console.log(_stamptime);
      var now = new Date();
      var timezone = now.getTimezoneOffset();
      var stampTime = new Date(Date.parse(_stamptime) + timezone * 60 * 1000);

      console.log("프론트의 현재 시간");
      console.log(now);
      console.log("response에서 받아온 시간을 Date 객체로 변환한 시간");
      console.log(stampTime);
      return now > this.getResetDate(stampTime);
    },
    loadStamp: function(page_number) {
      let vm = this;
      var temp_stamps = [];
      axios
        .get("/loadstamp", {
          params: {
            page: page_number
          }
        })
        .then(function(response) {
          if (response.status == 200) {
            // totalPageNum = 총 스탬프 페이지 갯수
            var totalPageNum =
              parseInt(response.data.response_data.count / 15, 10) + 1;
            if (totalPageNum != page_number && page_number != 0) {
              // 요청받은 페이지가 최신 페이지가 아니라 과거의 페이지이다.
              vm.currentPage = page_number;
              vm.stampNum = 15;
            } else {
              // 요청받은 페이지가 최신 페이지이다. : page_number = totalPageNum or 0
              vm.currentPage = totalPageNum;
              vm.stampNum = response.data.response_data.count % 15;
            }

            var tempPages = [];
            console.log("스탬프 정보 받음");
            console.log(response);
            // Javascript has no range function.
            for (var i = 1; i < totalPageNum + 1; i++) {
              tempPages.push(i);
            }
            vm.pages = tempPages;
            // console.log(vm.pages);
            // console.log(vm.stampNum);

            for (var i = 0; i < vm.stampNum; i++) {
              console.log("값 할당중");
              temp_stamps.push({
                exist: 1,
                memo: response.data.response_data.stamp_list[i].memo,
                submit_time:
                  response.data.response_data.stamp_list[i].submitdate,
                idx: response.data.response_data.stamp_list[i].idx
              });
            }
            // exist=2 는 다음에 찍을 스탬프
            temp_stamps.push({
              exist: 2,
              memo: null,
              submit_time: null,
              idx: null
            });

            for (var i = vm.stampNum + 1; i < 15; i++) {
              console.log("제로값 할당중");
              temp_stamps.push({
                exist: 0,
                memo: null,
                submit_time: null,
                idx: null
              });
            }
            vm.stamps = temp_stamps;
            console.log(vm.stamps);
            if (response.data.response_data.last_stamp_date == "") {
              vm.last_stamp_date = new Date("1/1/1970");
            } else {
              vm.last_stamp_date = response.data.response_data.last_stamp_date;
            }
            console.log("response에서 받아온 last_stamp_date");
            console.log(vm.last_stamp_date);
          } else {
            console.log("스탬프 정보 받기 실패" + response);
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getResetDate: function(stampTime) {
      // 스탬프를 다시 찍을 수 있는 시간을 반환한다.
      if (stampTime.getHours() >= 5) {
        stampTime.setDate(stampTime.getDate() + 1);
      }
      return stampTime.setHours(5, 0, 0);
    },
    handleUpdate: function(isValid) {
      if (isValid == true) {
        console.log("스탬프 삭제 후 카드 갱신중");
        this.loadStamp(0);
        this.bubbleMsg = this.kokkoro_comment["DELETE_STAMP"];
      } else {
        console.log("스탬프 삭제 취소");
        this.bubbleMsg = this.kokkoro_comment["CANCEL_DELETION"];
      }
    }
  }
};
</script>

<style src="./../styles/Stamp.css"></style>

