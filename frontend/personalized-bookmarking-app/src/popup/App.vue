<template>
  <v-container id="app">
    <v-container v-if="authed == false" id="login">
      <v-row>
        <v-col class="d-flex align-center" cols="12">
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
        <v-col cols="12">
      </v-row>
      <v-row>
        <v-col cols="1"></v-col>
        <v-col cols="10">
          <v-text-field type="text" name="email" v-model="email" placeholder="Email"></v-text-field>
        </v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
      </v-row>
      <v-row>
        <v-col cols="1"></v-col>
        <v-col cols="10">
          <v-text-field type="password" name="password" v-model="password" placeholder="Password"></v-text-field>
        </v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
      </v-row>
      <v-row>
        <v-col cols="4"></v-col>
        <v-col cols="4">
          <v-btn type="button" v-on:click="login()">Login</v-btn>
        </v-col>
        <v-col cols="4"></v-col>
      </v-row>
    </v-container>
    <v-container v-else id="content">
      <vue-tabs>
        <v-tab title="Account">
          <v-row>
            <v-col cols="12">
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-toolbar>
                <v-spacer />
                <v-toolbar-title class="headline text-uppercase">
                  <h4>Hello, {{ user.email }}!</h4>
                </v-toolbar-title>
                <v-spacer />
              </v-toolbar>
            <v-col>
          </v-row>
          <v-row>
            <v-col cols="4"></v-col>
            <v-col cols="4">
              <v-btn type="button" v-on:click="logout()">Logout</v-btn>
            <v-col>
            <v-col cols="4"></v-col>
          </v-row>
        </v-tab>
        <v-tab title="New Bookmark">
          <v-row>
            <v-col cols="12">
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field type="text" name="bookmark_name" v-model="bookmark_name" placeholder="Bookmark Name"></v-text-field>
            </v-col>
          <v-row>
          <v-row>
            <v-col cols="4"></v-col>
            <v-col cols="4">
              <v-btn type="button" v-on:click="addBookmark()">Add</v-btn>
            </v-col>
            <v-col cols="4"></v-col>
          <v-row>
        </v-tab>
        <v-tab title="Search">
          <v-row>
            <v-col cols="12">
          </v-row>
          <v-row>
            <v-col cols="8">
              <v-text-field type="text" name="query" v-model="query" placeholder="Query"></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-select v-model="selected_top" :items="top_items" item-text="name" item-value="value" persistent-hint return-object single-line></v-select>
            </v-col>
          <v-row>
          <v-row>
            <v-col cols="4"></v-col>
            <v-col cols="4">
              <v-btn type="button" v-on:click="searchBookmarks()">Search</v-btn>
            </v-col>
            <v-col cols="4"></v-col>
          </v-row>
        </v-tab>
        <v-tab title="All Bookmarks">
          <v-row>
            <v-col cols="12">
          </v-row>
        </v-tab>
      </vue-tabs>
    </v-container>
    <v-snackbar v-model="snackbar"> {{ snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import {VueTabs, VTab} from 'vue-nav-tabs/dist/vue-tabs.js'
import 'vue-nav-tabs/themes/vue-tabs.css'
export default {
  components: {VueTabs, VTab},
  created: function() {
    // set current tab info
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      this.bookmark_name = tabs[0].title;
      this.bookmark_url = tabs[0].url;
    });
    // check if user is logged in
    chrome.runtime.sendMessage({command: "checkAuth"}, (response) => {
      console.log(response);
      if (response.status == 'success') {
        console.log("User is still logged in");
        this.user = response.message;
        this.authed = true;
      } else {
        console.log("User is logged out");
        this.user = null;
        this.authed = false;
      }
    });
  },
  data() {
    return {
      email: "",
      password: "",
      user: null,
      authed: false,
      bookmark_name: "",
      bookmark_url: "",
      query: "",
      selected_top: {name: 'Top5', value: 5},
      top_items: [
        {name: 'Top5', value: 5},
        {name: 'Top10', value: 10},
        {name: 'Top15', value: 15},
        {name: 'Top20', value: 20},
      ],
      snackbar: false,
      snackbar_text: "",
    }
  },
  methods: {
    login() {
      chrome.runtime.sendMessage({command: "login", data: {email: this.email, password: this.password}}, (response) => {
        if (response) {
          if (response.status == 'success') {
            console.log("Login Success");
            this.user = response.message;
            this.authed = true;
            console.log(this.user);
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
        if (response) {
          if (response.status == 'success') {
            console.log("Logout Success")
            this.user = null;
            this.authed = false;
          } else {
            this.snackbar_text = "Error logging out! Please try again.";
            this.snackbar = true;
          }
        } else {
          this.snackbar_text = "Error logging out! Please try again.";
          this.snackbar = true;
        }
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
