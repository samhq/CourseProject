<template>
  <div>
    <p>Hello world!</p>
  </div>
</template>

<script>
export default {
  created: function() {
    // check if user is logged in
    chrome.runtime.sendMessage({command: "checkAuth"}, (response) => {
      console.log(response);
      if (response.status == 'success') {
        // redirect to user's content page
      } else {
        // stay on current login page
      }
    });
  },
  data() {
    return {
      email: "",
      password: ""
    }
  },
  methods: {
    login() {
      chrome.runtime.sendMessage({command: "login", data: {email: this.email, password: this.password}}, (response) => {
        console.log(response);
        if (response.status == 'success') {
          // redirect to user's content page
        } else {
          // handle errors
        }
      });
    },
    logout() {
      chrome.runtime.sendMessage({command: "logout"}, (response) => {
        console.log(response);
      });
    }
  }
}
</script>

<style lang="scss" scoped>
p {
  font-size: 20px;
}
</style>
