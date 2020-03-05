<template>
  <div id="Validation"></div>
</template>


<script>
import axios from "axios";

export default {
  name: "Validation",
  created: function() {
    var token = window.location.pathname.split("/").pop();
    const SEND_VALIDATE_EMAIL_SUCCESS = 20;
    axios
      .get("/id-validation/" + token)
      .then(function(response) {
        if (
          response.status === 200 &&
          response.data.code === SEND_VALIDATE_EMAIL_SUCCESS
        ) {
          alert("이메일 인증 완료");
          window.location.href = "/main";
        } else {
          alert("이메일 인증 오류");
          window.location.href = "/main";
        }
      })
      .catch(function(error) {
        alert(error);
        window.location.href = "/main";
      });
  }
  // data() {
  //   return {
  //     id: "",
  //     password: "",
  //     email: ""
  //   };
  // }
};
</script>
