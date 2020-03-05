<template>
  <div id="Signup">
    <div id="loginTitle">ARUJISAMA</div>
    <div class="koreanFont" id="signUpBox">
      <p>
        ID: &nbsp;
        <input v-model="id" placeholder="ID" />
        <button class="koreanFont idCheckButton" @click="idCheck">ID 중복확인</button>
      </p>
      <p class="noticeFontSize">* ID는 2자 이상 20자 이하 영문, 숫자</p>
      <p>
        비밀번호: &nbsp;
        <input type="password" v-model="password" placeholder="PW" />
      </p>
      <p>
        비밀번호 확인: &nbsp;
        <input type="password" v-model="password_confirm" />
      </p>
      <p class="noticeFontSize">* 비밀번호는 8자 이상 20자 이하 영문, 숫자</p>
      <p>
        이름: &nbsp;
        <input v-model="name" placeholder="name" />
      </p>
      <p class="buttonPosition">
        <button class="koreanFont" @click="returnMain">돌아가기</button>
        &nbsp; &nbsp;
        <button class="koreanFont" @click="signUpCheck">회원가입</button>
      </p>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import router from "../router";

export default {
  name: "Signup",
  data() {
    return {
      id: "",
      password: "",
      password_confirm: "",
      name: "",
      isIdChecked: false
    };
  },
  created: function() {
    this.isIdChecked = false;
  },
  methods: {
    isValidPassword: function(password) {
      if (password.length < 8 || password.length > 20) {
        alert("비밀번호의 길이를 확인해 주세요.");
        return false;
      }
      return true;
    },
    isValidName: function(name) {
      const namePattern = /^[a-z0-9가-힣]+$/i;
      if (name.length < 2 || name.length > 30) {
        alert("이름의 길이를 확인해 주세요.");
        return false;
      }
      if (!namePattern.test(name)) {
        alert("이름 형식을 확인해 주세요.");
        return false;
      }
      return true;
    },
    signUpCheck: function() {
      if (!this.isIdChecked) {
        alert("id 중복체크를 먼저 해주세요.");
        return;
      }

      var validation =
        this.isValidPassword(this.password) && this.isValidName(this.name);

      if (validation) {
        axios
          .get("/signup", {
            params: {
              id: this.id,
              pw: this.password,
              name: this.name
            }
          })
          .then(function(response) {
            if (response.status == 200 && response.data.code == 8) {
              console.log("회원가입 완료");
              console.log(response);
              router.push({ name: "Login" });
              alert("회원가입이 성공적으로 이루어졌습니다!");
            }
          })
          .catch(function(error) {
            console.log(error.response);
            alert("서버로부터 데이터를 받아오는 데 문제가 있었습니다.");
          });
      }
    },
    idCheck: function() {
      let vm = this;
      var isValidId = /^[a-z0-9]+$/i;
      if (
        this.id.length < 2 ||
        this.id.length > 20 ||
        this.id == "testid" ||
        !isValidId.test(this.id)
      ) {
        alert("ID 양식을 체크해주세요.");
        return;
      }
      axios
        .get("/idexistcheck", {
          params: {
            id: vm.id
          }
        })
        .then(function(response) {
          switch (response.data.code) {
            case 1:
              alert("사용 가능한 ID입니다!");
              vm.isIdChecked = true;
              break;
            case 2:
              alert("이미 존재하는 ID입니다.");
              break;
            case 3:
              alert(
                "서버 관리자에게 문의해 주세요. 에러 코드: ID_MORE_THAN_ONE"
              );
              break;
            case 4:
              alert("id는 2자 이상, 20자 이하의 영문 및 숫자로 해주세요.");
          }
        })
        .catch(function(error) {
          alert("서버와의 통신에 문제가 발생했습니다.");
          console.log(error);
        });
    },
    returnMain: function() {
      router.push({ name: "Login" });
    }
  }

  // email 인증용으로 나중에 사용할 코드임.
  // isValidEmail: function(email) {
  //   const emailPattern = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
  //   if (email.length > 50) {
  //     alert("이메일의 길이가 너무 깁니다.");
  //     return false;
  //   }
  //   if (!emailPattern.test(email)) {
  //     alert("이메일 형식을 확인해 주세요.");
  //     return false;
  //   }
  //   return true;
  // },
};
</script>
<style src="./../styles/Signup.css"></style>
