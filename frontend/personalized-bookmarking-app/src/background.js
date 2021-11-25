import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "firebase/auth";
import configJson from "@/config.json";

const app = initializeApp(configJson.firebaseConfig);
const auth = getAuth();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.command == "checkAuth") {
    onAuthStateChanged(auth, (user) => {
      if (user) {
        sendResponse({status: "success", message: user});
      } else {
        sendResponse({status: "no-auth", message: null});
      }
    });
  }

  if (message.command == "register") {
    var email = message.data.email;
    var password = message.data.password;
    createUserWithEmailAndPassword(auth, email, password).then((userCredential) => {
      const user = userCredential.user;
      sendResponse({status: "success", message: user});
    }).catch((error) => {
      sendResponse({status: "error", message: error});
    });
  }

  if (message.command == "login") {
    var email = message.data.email;
    var password = message.data.password;
    signInWithEmailAndPassword(auth, email, password).then((userCredential) => {
      const user = userCredential.user;
      sendResponse({status: "success", message: user});
    }).catch((error) => {
      sendResponse({status: "error", message: error});
    });
  }

  if (message.command == "logout") {
    signOut(auth).then(() => {
      sendResponse({status: "success", message: true});
    }).catch((error) => {
      sendResponse({status: "error", message: error});
    });
  }

  return true;
});