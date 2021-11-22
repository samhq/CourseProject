<template>
  <v-container id="login">
    <v-row>
      <v-col cols="12">
      <v-toolbar>
        <v-spacer />
        <v-toolbar-title class="headline text-uppercase">
          <h4>Welcome to PBSE! Please login.</h4>
        </v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="1"></v-col>
      <v-col cols="10"><v-text-field type="text" name="username" v-model="email" placeholder="Email"></v-text-field></v-col>
      <v-col cols="1"></v-col>
    </v-row>
    <v-row>
      <v-col cols="1"></v-col>
      <v-col cols="10"><v-text-field type="password" name="password" v-model="password" placeholder="Password"></v-text-field></v-col>
      <v-col cols="1"></v-col>
    </v-row>
    <v-row>
      <v-col cols="4"></v-col>
      <v-col cols="4"><v-btn type="button" v-on:click="login()">Login</v-btn></v-col>
      <v-col cols="4"></v-col>
    </v-row>
    <v-snackbar v-model="snackbar"> {{ snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  created: function() {
    // check if user is logged in
    chrome.runtime.sendMessage({command: "checkAuth"}, (response) => {
      console.log(response);
      if (response.status == 'success') {
        // redirect to user's content page
      }
    });
  },
  data() {
    return {
      email: "",
      password: "",
      snackbar: false,
      snackbar_text: "",
    }
  },
  methods: {
    login() {
      chrome.runtime.sendMessage({command: "login", data: {email: this.email, password: this.password}}, (response) => {
        console.log(response);
        if (response) {
          if (response.status == 'success') {
            // redirect to user's content page
          } else {
            this.snackbar_text = "Error logging in! Please try again.";
            this.snackbar = true;
          }
        } else {
          this.snackbar_text = "Error logging in! Please try again.";
          this.snackbar = true;
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

<style scoped>
p {
  font-size: 20px;
}
</style>
