<template>
  <div id="login" v-if="!(islogin)">
    <p style="text-align: center;">
      <img src="./../assets/main.png" />
    </p>
    <div id="loginTitle">ARUJISAMA</div>
    <div id="mainBox">
      <div id="idpw">
        ID
        <br />PW
      </div>
      <div id="textInput">
        <p>
          <input class="textInputSize" v-model="id" />
        </p>
        <p>
          <input class="textInputSize" type="password" v-model="password" />
        </p>
      </div>
      <div id="loginButton">
        <button class="koreanFont loginButtonSize" v-on:click="login">로그인</button>
      </div>
      <div id="otherButtons">
        <p>
          <!-- 계정찾기 기능 구현 안됨
          <button class="koreanFont otherButtonSize" v-on:click="forgot">계정찾기</button>
          -->
          <button class="koreanFont otherButtonSzie" v-on:click="signUp">회원가입</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import router from "../router";

export default {
  name: "Login",
  data() {
    return {
      id: "",
      password: "",
      token: "",
      islogin: true
    };
  },
  created() {
    var vm = this;
    axios
      .get("/tokencheck")
      .then(function(response) {
        if (response.status === 200 && response.data.code === 9) {
          console.log("토큰 유효. stamp로 이동");
          router.push({ name: "Stamp" });
        } else {
          console.log("토큰 유효하지 않음" + response);
          vm.islogin = false;
        }
      })
      .catch(function(error) {
        console.log(error.response);
        vm.islogin = false;
      });
  },
  mounted() {
    window.addEventListener("keyup", this.enterEvent);
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.enterEvent);
  },

  methods: {
    login: function(id, password) {
      var self = this;
      console.log("로그인 시도");
      axios
        .get("/login", {
          params: {
            id: this.id,
            pw: this.password
          }
        })
        .then(function(response) {
          console.log(response);

          if (response.status === 200 && response.data.code === 5) {
            console.log("정상 로그인");
            localStorage.setItem("token", response.data.access_token);
            router.push({ name: "Stamp" });
          }
        })
        .catch(function(error) {
          console.log(error);
          console.log(error.response.data);
          alert(
            "에러 코드:" +
              error.response.data.code +
              "\n" +
              error.response.data.notation
          );
        });
    },
    signUp: function() {
      console.log("회원가입 시도");
      router.push({ name: "Signup" });
    },
    forgot: function() {
      router.push({ name: "Forget" });
    },
    enterEvent: function(event) {
      const ENTER = 13;
      if (event.keyCode === ENTER) {
        this.login();
      }
    }
  }
};
</script>

<style src="./../styles/Login.css"></style>

