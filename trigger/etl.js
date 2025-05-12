import { schedules, logger } from "@trigger.dev/sdk/v3";
import { exec } from "child_process";
import { join } from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const projectRoot = process.cwd();

export const etlTask = schedules.task({
  id: "etl-pipeline",
  name: "ETL Pipeline Schedule",
  schedule: "0 */6 * * *", // Run every 6 hours
  maxDuration: 1000,
  async run(payload) {
    logger.info("🚀 Starting ETL pipeline");
    const scriptPath = join(projectRoot, "etl", "Master.py");
    logger.info(`📂 Executing script: ${scriptPath}`);

    try {
      await new Promise((resolve, reject) => {
        const pythonProcess = exec(`python "${scriptPath}"`, {
          cwd: projectRoot,
        });

        const cleanMessage = (line) => {
          return line
            .replace(/\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}\s-\s/, "")
            .replace("ETL-Pipeline - ", "")
            .trim();
        };

        pythonProcess.stdout.on("data", (data) => {
          data.toString().split("\n").forEach((line) => {
            if (!line.trim()) return;
            const message = cleanMessage(line);
            if (line.includes("- ERROR -")) {
              logger.error(`${message.replace("ERROR - ", "")}`);
            } else if (line.includes("- WARNING -")) {
              logger.warn(`${message.replace("WARNING - ", "")}`);
            } else {
              logger.info(`${message}`);
            }
          });
        });

        pythonProcess.stderr.on("data", (data) => {
          data.toString().split("\n").forEach((line) => {
            if (!line.trim()) return;
            const message = cleanMessage(line);
            if (line.includes("- ERROR -")) {
              logger.error(`${message.replace("ERROR - ", "")}`);
            } else if (line.includes("- WARNING -")) {
              logger.warn(`${message.replace("WARNING - ", "")}`);
            } else if (line.includes("- INFO -")) {
              logger.info(`${message.replace("INFO - ", "")}`);
            } else {
              logger.info(`${message}`);
            }
          });
        });

        pythonProcess.on("close", (code) => {
          if (code === 0) {
            logger.info("✅ Python script completed successfully");
            resolve();
          } else {
            logger.error(`❌ Python script failed with code ${code}`);
            reject(new Error(`Process exited with code ${code}`));
          }
        });

        pythonProcess.on("error", (error) => {
          logger.error(`❌ Failed to start Python process: ${error.message}`);
          reject(error);
        });
      });

      logger.info("🏁 ETL pipeline completed successfully");
    } catch (error) {
      logger.error(`🚩 ETL pipeline failed: ${error.message}`);
      throw error;
    } finally {
      logger.info("ETL pipeline finished");
    }
  },
});