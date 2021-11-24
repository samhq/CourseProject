<template>
  <v-app id="app">
    <v-container v-if="authed == false" id="login">
      <v-row>
        <v-col class="d-flex align-center" cols="12">
          <v-toolbar>
            <v-spacer />
            <v-toolbar-title class="headline text-uppercase">
              <h5>Welcome to PBSE! Please login.</h5>
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
        <v-col cols="2"></v-col>
        <v-col cols="3">
          <v-btn type="button" v-on:click="login()">Login</v-btn>
        </v-col>
        <v-col cols="1"></v-col>
        <v-col cols="4">
          <v-btn type="button" v-on:click="register()">Register</v-btn>
        </v-col>
        <v-col cols="2"></v-col>
      </v-row>
    </v-container>
    <v-container v-else id="content">
      <vue-tabs @tab-change="handleTabChange">
        <v-tab title="Welcome">
          <v-row>
            <v-col cols="12">
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-toolbar>
                <v-spacer />
                <v-toolbar-title class="headline text-uppercase">
                  <h6>Hello, {{ user.email }}</h6>
                </v-toolbar-title>
                <v-spacer />
              </v-toolbar>
            <v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field type="text" name="bookmark_name" v-model="bookmark_name" placeholder="Bookmark Name"></v-text-field>
            </v-col>
          <v-row>
          <v-row>
            <v-col cols="2"></v-col>
            <v-col cols="4">
              <v-btn type="button" v-on:click="addBookmark()">Add Bookmark</v-btn>
            </v-col>
            <v-col cols="1">
            </v-col>
            <v-col cols="3">
              <v-btn type="button" v-on:click="logout()">Logout</v-btn>
            <v-col>
            <v-col cols="2"></v-col>
          <v-row>
        </v-tab>
        <v-tab title="Search">
          <v-row>
            <v-col cols="12">
          </v-row>
          <v-row>
            <v-col cols="9">
              <v-text-field type="text" name="query" v-model="query" placeholder="Query"></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-select :items="top_items" item-text="name" item-value="value" v-model="selected_top"></v-select>
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
  </v-app>
</template>

<script>
import {VueTabs, VTab} from "vue-nav-tabs/dist/vue-tabs.js"
import "vue-nav-tabs/themes/vue-tabs.css"
export default {
  components: {VueTabs, VTab},
  created: function() {
    var vm = this;
    // set current page title as bookmark name
    vm.setTitleAsBookmarkName();
    // check if user is logged in
    chrome.runtime.sendMessage({command: "checkAuth"}, (response) => {
      if (response.status == "success") {
        vm.user = response.message;
        vm.authed = true;
      } else {
        vm.user = null;
        vm.authed = false;
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
      selected_top: {name: "Top5", value: 5},
      top_items: [
        {name: "Top5", value: 5},
        {name: "Top10", value: 10},
        {name: "Top15", value: 15},
        {name: "Top20", value: 20},
      ],
      snackbar: false,
      snackbar_text: "",
    }
  },
  methods: {    
    register() {
      var vm = this;
      chrome.runtime.sendMessage({command: "register", data: {email: vm.email, password: vm.password}}, (response) => {
        if (response) {
          if (response.status == "success") {
            vm.user = response.message;
            vm.authed = true;
            vm.snackbar_text = "Successfully registered and logged in.";
            vm.snackbar = true;
            console.log(vm.user);
          } else {
            if (response.message.code == "auth/weak-password"){
              vm.snackbar_text = "The password provided is too weak.";
            } else if (response.message.code == "auth/email-already-in-use") {
              vm.snackbar_text = "The account already exists for that email.";
            } else {
              vm.snackbar_text = "Error in registration, please try again later.";
            }
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error in registration, please try again later.";
          vm.snackbar = true;
        }
      });
    },
    login() {
      var vm = this;
      chrome.runtime.sendMessage({command: "login", data: {email: vm.email, password: vm.password}}, (response) => {
        if (response) {
          if (response.status == "success") {
            vm.user = response.message;
            vm.authed = true;
            vm.snackbar_text = "Successfully logged in.";
            vm.snackbar = true;
            console.log(vm.user);
          } else {
            if (response.message.code == "auth/user-not-found"){
              vm.snackbar_text = "No user found for that email.";
            } else if (response.message.code == "auth/wrong-password") {
              vm.snackbar_text = "Wrong password provided for that user.";
            } else {
              vm.snackbar_text = "Error logging in, please try again later.";
            }
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error logging in, please try again later.";
          vm.snackbar = true;
        }
      });
    },
    logout() {
      var vm = this;
      chrome.runtime.sendMessage({command: "logout"}, (response) => {
        if (response) {
          if (response.status == "success") {
            vm.user = null;
            vm.authed = false;
          } else {
            vm.snackbar_text = "Error logging out! Please try again.";
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error logging out! Please try again.";
          vm.snackbar = true;
        }
      });
    },
    handleTabChange(tabIndex, newTab, oldTab){
      if (newTab.tabId == "Welcome") {
        this.setTitleAsBookmarkName();
      }
      if (newTab.tabId == "All Bookmarks") {
        // retrieve bookmarks from API and update all_bookmarks variable
      }
    },
    setTitleAsBookmarkName(){
      var vm = this;
      chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        vm.bookmark_name = tabs[0].title;
        vm.bookmark_url = tabs[0].url;
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
