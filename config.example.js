// Copy this file to config.js and include it before index.html script block if needed.
// In plain static hosting, you can add:
// <script src="config.js"></script>
window.ACOUSTIC_GUARD_CONFIG = {
  edgeNodeCount: 2,
  firebase: {
    apiKey: 'YOUR_FIREBASE_API_KEY',
    projectId: 'YOUR_FIREBASE_PROJECT_ID',
    databaseURL: 'https://YOUR_PROJECT.firebaseio.com',
    storageBucket: 'YOUR_PROJECT.appspot.com',
    messagingSenderId: '',
    appId: '',
    measurementId: ''
  },
  tomtomApiKey: 'YOUR_TOMTOM_API_KEY',
  tomtomRoutePoints: {
    from: '12.9716,77.5946',
    to: '12.9760,77.6033'
  },
  yamnet: {
    localUrl: '',
    remoteUrl: 'https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json',
    timeoutMs: 12000
  }
};
