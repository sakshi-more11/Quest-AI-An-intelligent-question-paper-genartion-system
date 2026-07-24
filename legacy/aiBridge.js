const { spawn } = require("child_process");
const path = require("path");

const PYTHON_COMMAND = process.env.PYTHON_COMMAND || (process.platform === "win32" ? "python" : "python3");
const PYTHON_ARGS = [];

function runAiAction(action, payload, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const cwd = path.join(__dirname, "..");
    const child = spawn(PYTHON_COMMAND, [...PYTHON_ARGS, "-m", "backend.ai.cli"], {
      cwd,
      env: process.env,
      stdio: ["pipe", "pipe", "pipe"]
    });

    let stdout = "";
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error(`AI pipeline timed out while running ${action}.`));
    }, timeoutMs);

    child.stdout.on("data", chunk => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", chunk => {
      stderr += chunk.toString();
    });
    child.on("error", error => {
      clearTimeout(timer);
      reject(error);
    });
    child.on("close", code => {
      clearTimeout(timer);
      if (code !== 0) {
        return reject(new Error(stderr || `AI pipeline exited with code ${code}.`));
      }
      try {
        resolve(JSON.parse(stdout || "{}"));
      } catch {
        reject(new Error(`AI pipeline returned invalid JSON. ${stderr}`));
      }
    });

    child.stdin.end(JSON.stringify({ action, payload }));
  });
}

module.exports = {
  runAiAction
};
