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
        <v-col cols="12"></v-col>
      </v-row>
      <v-row>
        <v-col cols="1"></v-col>
        <v-col cols="10">
          <v-text-field type="text" name="email" v-model="email" placeholder="Email"></v-text-field>
        </v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row>
        <v-col cols="12"></v-col>
      </v-row>
      <v-row>
        <v-col cols="1"></v-col>
        <v-col cols="10">
          <v-text-field type="password" name="password" v-model="password" placeholder="Password"></v-text-field>
        </v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row>
        <v-col cols="12"></v-col>
      </v-row>
      <v-row>
        <v-col cols="2"></v-col>
        <v-col cols="3">
          <v-btn type="button" color="primary" @click="login()">Login</v-btn>
        </v-col>
        <v-col cols="2"></v-col>
        <v-col cols="4">
          <v-btn type="button" color="secondary" @click="register()">Register</v-btn>
        </v-col>
        <v-col cols="1"></v-col>
      </v-row>
    </v-container>
    <v-container v-else id="content">
      <vue-tabs ref="tabs" @tab-change="handleTabChange">
        <v-tab title="Welcome">
          <v-row>
            <v-col cols="12"></v-col>
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
              <v-btn type="button" color="primary" @click="addBookmark()">Add Bookmark</v-btn>
            </v-col>
            <v-col cols="1"></v-col>
            <v-col cols="3">
              <v-btn type="button" color="error" @click="logout()">Logout</v-btn>
            <v-col>
            <v-col cols="2"></v-col>
          <v-row>
        </v-tab>
        <v-tab title="Search">
          <v-row>
            <v-col cols="12"></v-col>
          </v-row>
          <v-row>
            <v-col cols="9">
              <v-text-field type="text" name="query" v-model="query" placeholder="Query"></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-select :items="top_items" item-text="name" item-value="value" v-model="selected_top" return-object></v-select>
            </v-col>
          <v-row>
          <v-row>
            <v-col cols="2"></v-col>
            <v-col cols="3">
              <v-btn type="button" color="primary" @click="switchTab(2); searchBookmarks()">Search</v-btn>
            </v-col>
            <v-col cols="4">
              <v-btn type="button" color="secondary" @click="switchTab(2); loadAllBookmarks(true)">All Bookmarks</v-btn>
            <v-col>
            <v-col cols="1"></v-col>
            <v-col cols="2"></v-col>
          </v-row>
        </v-tab>
        <v-tab title="Bookmarks">
          <v-row>
            <v-col cols="12"></v-col>
          </v-row>
          <v-row>
            <v-col class="d-flex align-center" cols="12">
              <v-toolbar dense>
                <v-spacer />
                <v-toolbar-title class="headline text-uppercase">
                  <h6>{{ bookmarks.length }} bookmarks returned</h6>
                </v-toolbar-title>
                <v-spacer />
              </v-toolbar>
            </v-col>
          </v-row>
          <v-row dense v-for="bookmark in bookmarks" :key="bookmark.name">
            <v-col no-gutters cols="10">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn v-if="bookmark.name.length <= 30" tile block depressed style="text-transform:none !important;justify-content: space-between !important;padding: 0 8px;" @click="openUrl(bookmark.url)">
                    <span>{{ bookmark.name }}</span>
                    <span class="score" v-if="bookmark.score">Score: {{ bookmark.score.toFixed(2) }}</span>
                  </v-btn>
                  <v-btn v-else tile block depressed style="text-transform:none !important;justify-content: space-between !important;padding: 0 8px;" @click="openUrl(bookmark.url)" v-bind="attrs" v-on="on">
                    <span>{{ bookmark.name.substring(0, 30) + "..." }}</span>
                    <span class="score" v-if="bookmark.score">Score: {{ bookmark.score.toFixed(2) }}</span>
                  </v-btn>
                </template>
                <span>{{ bookmark.name }}</span>
              </v-tooltip>
            </v-col>
            <v-col dense cols="2" @click="deleteBookmark(bookmark)">
              <v-btn tile block depressed color="error">
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </v-col>
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
import api from "@/services/api";
import {VueTabs, VTab} from "vue-nav-tabs/dist/vue-tabs.js";
import "vue-nav-tabs/themes/vue-tabs.css";
export default {
  components: {VueTabs, VTab},
  created: function() {
    var vm = this;
    // set current page title as bookmark name
    vm.setTitleAsBookmarkName();
    // check if user is logged in
    chrome.runtime.sendMessage({command: "checkAuth"}, (response) => {
      if (response.status == "success") {
        vm.user = response.message.user;
        vm.token = response.message.token;
        console.log(vm.user);
        console.log(vm.token);
        vm.authed = true;
        // retrieve all bookmarks and display them in the bookmarks tab upon initlal page load
        vm.loadAllBookmarks(false);
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
      token: null,
      authed: false,
      bookmark_name: "",
      bookmark_url: "",
      bookmarks: [],
      query: "",
      selected_top: {name: "Top5", value: 5},
      top_items: [
        {name: "Top5", value: 5},
        {name: "Top10", value: 10},
        {name: "Top15", value: 15},
        {name: "Top20", value: 20},
        {name: "Top25", value: 25},
      ],
      snackbar: false,
      snackbar_text: "",
      tabName: "",
      hover: false,
    }
  },
  methods: {    
    register() {
      var vm = this;
      chrome.runtime.sendMessage({command: "register", data: {email: vm.email, password: vm.password}}, (response) => {
        if (response) {
          if (response.status == "success") {
            vm.user = response.message.user;
            vm.token = response.message.token;
            vm.authed = true;
            vm.snackbar_text = "Successfully registered and logged in.";
            vm.snackbar = true;
            console.log("Successfully registered and logged in.");
            console.log(vm.user);
          } else {
            if (response.message.code == "auth/weak-password"){
              vm.snackbar_text = "The password provided is too weak.";
            } else if (response.message.code == "auth/email-already-in-use") {
              vm.snackbar_text = "The account already exists for that email.";
            } else {
              vm.snackbar_text = "Error in registration.";
            }
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error in registration.";
          vm.snackbar = true;
        }
      });
    },
    login() {
      var vm = this;
      chrome.runtime.sendMessage({command: "login", data: {email: vm.email, password: vm.password}}, (response) => {
        if (response) {
          if (response.status == "success") {
            vm.user = response.message.user;
            vm.token = response.message.token;
            vm.authed = true;
            vm.loadAllBookmarks(false);
            vm.snackbar_text = "Successfully logged in.";
            vm.snackbar = true;
            console.log("Successfully logged in.");
            console.log(vm.user);
          } else {
            if (response.message.code == "auth/user-not-found"){
              vm.snackbar_text = "No user found for that email.";
            } else if (response.message.code == "auth/wrong-password") {
              vm.snackbar_text = "Wrong password provided for that user.";
            } else {
              vm.snackbar_text = "Error logging in.";
            }
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error logging in.";
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
            vm.token = null;
            vm.authed = false;
          } else {
            vm.snackbar_text = "Error logging out.";
            vm.snackbar = true;
          }
        } else {
          vm.snackbar_text = "Error logging out.";
          vm.snackbar = true;
        }
      });
    },
    handleTabChange(tabIndex, newTab, oldTab){
      if (newTab.tabId == "Welcome") {
        this.setTitleAsBookmarkName();
      }
    },
    setTitleAsBookmarkName(){
      var vm = this;
      chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        vm.bookmark_name = tabs[0].title;
        vm.bookmark_url = tabs[0].url;
      });
    },
    openUrl(url) {
      chrome.tabs.create({ url: url, active: false });
    },
    switchTab(tab_index){
      this.$refs.tabs.navigateToTab(tab_index)
    },
    addBookmark() {
      var vm = this;
      const config = {
        headers: {'Content-Type': 'multipart/form-data', 'Authorization': vm.token}
      };
      var body = new FormData();
      body.append('bookmark_name', vm.bookmark_name);
      body.append('webpage_url', vm.bookmark_url);
      api.post("/add_bookmark", body, config).then((response) => {
        console.log(response);
        vm.snackbar_text = "Sucessfully added bookmark.";
        vm.snackbar = true;
      }).catch((error) => {
        console.log(error);
        vm.snackbar_text = "Error adding bookmark.";
        vm.snackbar = true;
      });
    },
    deleteBookmark(delete_bookmark) {
      var vm = this;
      const config = {
        headers: {'Content-Type': 'multipart/form-data', 'Authorization': vm.token}
      };
      var body = new FormData();
      body.append('bookmark_id', delete_bookmark.id);
      api.post("/delete_bookmark", body, config).then((response) => {
        console.log(response);
        for (let bookmark of vm.bookmarks) {
          if (bookmark.id == delete_bookmark.id) {
            vm.bookmarks = vm.bookmarks.filter(item => item.id !== bookmark.id);
            break;
          }
        }
        vm.snackbar_text = "Sucessfully deleted bookmark.";
        vm.snackbar = true;
      }).catch((error) => {
        console.log(error);
        vm.snackbar_text = "Error deleting bookmark.";
        vm.snackbar = true;
      });
    },
    searchBookmarks() {
      var vm = this;
      const config = {
        headers: {'Content-Type': 'multipart/form-data', 'Authorization': vm.token}
      };
      var body = new FormData();
      body.append('query', vm.query);
      body.append('top_n', vm.selected_top.value);
      console.log(vm.selected_top.value);
      api.post("/search_bookmark", body, config).then((response) => {
        console.log(response);
        const bookmarks_json = response.data.bookmarks;
        var bookmarks = [];
        for (const [key, value] of Object.entries(bookmarks_json)) {
          bookmarks.push({"id": key, "name": value.title, "url": value.url, "score": value.score});
        }
        vm.bookmarks = bookmarks;
        vm.snackbar_text = "Bookmark search results retrieved successfully.";
        vm.snackbar = true;
      }).catch((error) => {
        console.log(error);
        vm.snackbar_text = "Error retrieving bookmark search results.";
        vm.snackbar = true;
      });
    },
    loadAllBookmarks(messageBoolean) {
      var vm = this;
      const config = {
        headers: {'Authorization': vm.token}
      };
      api.get("/get_all_bookmarks", config).then((response) => {
        console.log(response);
        const bookmarks_json = response.data.bookmarks;
        var bookmarks = [];
        for (const [key, value] of Object.entries(bookmarks_json)) {
          bookmarks.push({"id": key, "name": value.title, "url": value.url});
        }
        vm.bookmarks = bookmarks;
        if (messageBoolean){
          vm.snackbar_text = "All bookmarks retrieved successfully.";
          vm.snackbar = true;
        }
      }).catch((error) => {
        console.log(error);
        if (messageBoolean){
          vm.snackbar_text = "Error retrieving all bookmarks.";
          vm.snackbar = true;
        } else {
          vm.snackbar_text = "Error loading all bookmarks.";
          vm.snackbar = true;
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
.score {
  font-size: 9px;
  color: #999;
  font-style: italic;
}
</style>
