# CourseProject - Fall 2021

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## PBSE: Personalized Bookmark Search Engine

Most, if not all modern internet browsers such as Google Chrome offer a bookmark feature that allows users to retain website URLs for future reference. This makes it very convenient for users to access their favourite websites. However, as a bookmark list grows larger over time, users will have a hard time searching through it to find the relevant contents they want. Moreover, there isn't a way to search into the contents of those bookmarks as a bookmark only contains the URL and title of a particular web page. Thus, we are proposing a personalized bookmark search engine to address these shortcomings.

### Theme

Intelligent Browsing

### Members

- Gazi Muhammad Samiul Hoque (NetID: `ghoque2`) -  Captain
- Yuheng Xie (NetID: `yuhengx2`)
- Grace, Mu-Hui Yu (NetID: `muhuiyu2`)
- Ying-Chen Lee (NetID: `yclee6`)

---

## Tutorial Presentation

Our tutorial presentation is hosted on UIUC Box. You may view it [here](https://uofi.box.com/s/f5fd5acnr0edicrc94d207l9zu7peh8f).

---

## Simple Installation

To make the installation of our application simple, we have hosted our backend server [here](https://pbse-md7vc2dicq-as.a.run.app/). This backend endpoint is used by the Chrome extension frontend by default. If you wish to host your own backend server, refer to the "Advanced Installation" section.

The installation instructions are as follows:

1. Download or clone this repository and unzip it.
2. Open Google Chrome and enter <chrome://extensions/> in the address bar.
3. Click on the "Load unpacked" button in the upper left-hand corner.
4. Select the `.../frontend/personalized-bookmarking-app/dist` folder as the extension directory.
5. The extension is installed! Click on the jigsaw icon on the right side of the address bar to pin the bookmark extension (as represented by the book icon) to the toolbar.

You may use our demo account (email: demo@test.com, password: 123456) to log in into the app if you do not wish to register an account.

---

## Advanced Installation

### Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)

### 1. Setting up Firebase

If you wish to host the backend server by yourself on localhost, you would have to set up a Firebase account since the backend uses Firebase for authentication and storage.  To do this, first create a gmail account and then log in into the [Firebase console](https://console.firebase.google.com/).

Next, click on "Add project" and follow the steps to create a new Firebase project. You do not have to enable Google Analytics for this project.

Once your project is ready, you will be redirected to the Firebase admin dashboard. Click on "Authentication" on the sidebar and click on "Get Started". Go to the Sign-in method tab, click on "Email/Password" under "Native providers", tick enable for the "Email/Password" sign-in option and click "Save".

After that, you will need to create a Realtime database to store user bookmarks. Click on "Realtime Database" on the sidebar and click on "Create Database". Choose a Realtime Database location and select "Start in test mode" option for Security rules.

Subsequently, click on "Project Overview" on the sidebar and select "Web" in the "Get started by adding Firebase to your app" section. Provide a name for your app, and select the "Use npm" option under the "Add Firebase SDK section". Copy down the `const firebaseConfig` json fields as you would need it later.

### 2. Running the Flask backend server

Change directory to the `/backend` folder and install the required python modules using `pip install -r requirements.txt`.

Then, in `main.py`, replace the `host="0.0.0.0"` field with `host="127.0.0.1"`. You'll need two config files in the `/backend` directory for the backend to connect and use Firebase:

- `fbconfig.json`: Copy the `const firebaseConfig` json fields you have copied down earlier in the "Setting up Firebase" step in a new `fbconfig.json` file.
- `fbAdminConfig.json`: Go to your Firebase project, then `Project Settings` -> `Service Accounts` -> `Generate a new private key`. A new JSON file will be downloaded. Rename it to `fbAdminConfig.json` and save in the `/backend` directory.

Run the backend server using `python main.py`. The backend server will be hosted locally on <http://localhost:5000>.

### 3. Installing frontend modules

Change directory to the `/frontend/personalized-bookmarking-app` folder and install the required Node.js modules using `npm install`.

Similarly, replace the fields in `/src/config.json` with the `const firebaseConfig` json fields you have copied down earlier in the "Setting up Firebase" step.

### 4. Building frontend files

Finally, build the Chrome extension files using `npm run build`. The newly generated files will be located in the `/dist` folder. You may then refer to the ["Simple Installation"](#simple-installation) section to install the Chrome extension.

### 5. Deployment

To deploy the backend API service, you can try a few ways. We have used Google Cloud Run (GCP) to deploy our backend in a serverless, autoscaled and load-balanced environment. You can check the tutorial [Build and deploy a Python service](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python) for using Cloud Run. Alternatively, you can deploy the backend into any VM and setup the web server yourself.
