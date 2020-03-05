<template>
  <div id="Forget">
    <div class="koreanFont" id="IDfind">
      <p>
        이름: &nbsp;
        <input v-model="idfind_name" placeholder="이름" />
      </p>
      <p>
        E-mail: &nbsp;
        <input v-model="idfind_email" placeholder="email" />
      </p>
      <button class="koreanFont" @click="idFound">ID 찾기</button>
      <hr />
      <div class="koreanFont" id="PWchange">
        <p>
          아이디: &nbsp;
          <input v-model="pwfind_id" placeholder="ID" />
        </p>
        <p>
          이름: &nbsp;
          <input v-model="pwfind_name" placeholder="이름" />
        </p>
        <p>
          E-mail: &nbsp;
          <input v-model="pwfind_email" placeholder="email" />
        </p>
        <button class="koreanFont" @click="passwordChange">PW 변경</button>
        <p>
          <button class="koreanFont" @click="returnMain">돌아가기</button>
        </p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import router from "../router";

export default {
  name: "Forget",
  data() {
    return {
      idfind_name: "",
      idfind_email: "",
      pwfind_id: "",
      pwfind_name: "",
      pwfind_email: ""
    };
  },

  methods: {
    returnMain: function() {
      router.push({ name: "Login" });
    },
    idFound: function() {
      const FIND_ID_SUCCESS = 29;
      const FIND_ID_FAILED = 30;
      // /find-id?name=XXX&email=YYY
      var vm = this;
      axios
        .get("/find-id", {
          params: {
            name: vm.idfind_name,
            email: vm.idfind_email
          }
        })
        .then(function(response) {
          console.log(response);
          if (response.data.code == FIND_ID_SUCCESS) {
            alert("당신의 ID는 " + response.data.response_data.id + "입니다");
          } else if (response.data.code == FIND_ID_FAILED) {
            alert("입력한 값이 맞지 않습니다.");
          }
        })
        .catch(function(error) {
          if (error.response.data.code == FIND_ID_FAILED) {
            alert("입력한 값이 맞지 않습니다.");
          } else console.log(error);
        });
      console.log("id 찾기");
    },
    passwordChange: function() {
      console.log("비밀번호 초기화");
    }
  }
};
// style에선 임시로 signup의 css 공유중
</script>
<style src="./../styles/Signup.css"></style>
