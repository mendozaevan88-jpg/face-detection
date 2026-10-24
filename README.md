# Face Presence Monitor

A single-file web page that counts faces in front of your device's camera, in the browser. It does not identify anyone, and nothing is uploaded or saved.

## Run locally
1. Put `index.html` in a folder and run `python -m http.server 8000` in that folder.
2. Open `http://localhost:8000` in Chrome or Firefox.
3. Tick the consent box, click Start camera, and allow the camera.

The page shows a checklist (secure page, library, model, camera) so you can see which step fails.

## Publish with GitHub Pages
1. Create a free GitHub account and a new public repository.
2. Upload `index.html`, `README.md`, and `LICENSE`.
3. Go to Settings, then Pages. Choose the `main` branch and `/ (root)`, and save.
4. Share `https://<your-username>.github.io/<repository-name>/`.

## Responsible use
- All processing happens in the browser. No video or images leave the device.
- Only use it where the camera owner or everyone in view agrees to be counted.
- Faces are personal data. Laws such as the Philippines' Data Privacy Act of 2012 or the EU GDPR may apply if you collect or store them. Do not use this to secretly monitor people.

## Third-party components
- MediaPipe Tasks Vision (Apache-2.0), loaded from the jsDelivr CDN.
- MediaPipe BlazeFace face detector model, loaded from Google's model storage. Check its license terms before redistributing the model.

## License
MIT. See LICENSE.
