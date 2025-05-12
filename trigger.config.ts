import { defineConfig } from "@trigger.dev/sdk/v3";
import { pythonExtension } from "@trigger.dev/python/extension";
import { BuildContext, BuildExtension } from "@trigger.dev/core/v3/build"; // added

function predownloadNLTKData(): BuildExtension {
  return {
    name: "PredownloadNLTKData",
    onBuildComplete(context: BuildContext) {
      const instructions = [
        "RUN python -m nltk.downloader -d /opt/venv/nltk_data punkt",
        "RUN python -m nltk.downloader -d /opt/venv/nltk_data averaged_perceptron_tagger",
        "RUN python -m nltk.downloader -d /opt/venv/nltk_data stopwords", // added download for stopwords
        // Add more NLTK data downloads as needed
      ];
      context.addLayer({
        id: "nltk-data",
        image: { instructions },
      });
    },
  };
}

export default defineConfig({
  project: "proj_imcawmqalaarepkrsjmx",
  dirs: ["./trigger"],
  retries: {
    enabledInDev: false,
    default: {
      maxAttempts: 3,
      minTimeoutInMs: 1000,
      maxTimeoutInMs: 10000,
      factor: 2,
      randomize: true,
    },
  },
  maxDuration: 1000,
  machine: "small-1x",
  build: {
    external: ["child_process", "path"],
    extensions: [
      pythonExtension({
        requirementsFile: "./requirements.txt",
        devPythonBinaryPath: `venv/bin/python`,
        scripts: ["etl/**/*.py", "news_scraper/**/*.py", "setup.py"],
      }),
      predownloadNLTKData(), // added extension
    ],
  }
});
