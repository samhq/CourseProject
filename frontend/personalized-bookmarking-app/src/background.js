import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

// Firebase configuration
var firebaseConfig = {
  apiKey: "AIzaSyAM36yqurrk2ioTxKRMexHrXiaV7mZh0o4",
  authDomain: "pbse-df479.firebaseapp.com",
  projectId: "pbse-df479",
  storageBucket: "pbse-df479.appspot.com",
  messagingSenderId: "619390935453",
  appId: "1:619390935453:web:edca38724cffca328ecf74"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

chrome.runtime.onMessage.addListener((msg, sender, response) => {
  if (msg.command == 'checkAuth') {
    var user = firebase.auth().currentUser;
    if (user) {
      // User is signed in.
      response({type: "auth", status: "success", message: user});
    } else {
      // No user is signed in.
      response({type: "auth", status: "no-auth", message: false});
    }
  }
  if (msg.command == 'login') {
    console.log(msg.data);
    var email = msg.data.email;
    var password = msg.data.password;
    //Add seperate values for auth info here instead of fixed variables...
    firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      console.log(error);

      response({type: "auth", status: "error", message: error});
      // ...
    });
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        // User is signed in.
        console.log(user);
        response({type: "auth", status: "success", message: user});
      } else {
        // No user is signed in.
      }
    });
  }
  if (msg.command == 'logout') {
    firebase.auth().signOut().then(function() {
      // Sign-out successful.
      response({type: "un-auth", status: "success", message: true});
    }, function(error) {
      // An error happened.
      response({type: "un-auth", status: "false", message: error});
    });
  }

  return true;
});