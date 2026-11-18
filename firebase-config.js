/* Study Den — Firebase project settings for the hosted copy.
 *
 * Paste the config object Firebase gives you under
 *   Project settings -> Your apps -> Web app -> SDK setup and configuration.
 * Leave apiKey empty and the app simply saves on the device instead.
 *
 * These values are not secrets: a web app has to ship them, and what protects
 * your den is the Firestore rule in firestore.rules, which lets each signed-in
 * account read and write only its own document.
 */
window.STUDYDEN_FIREBASE = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: ""
};
