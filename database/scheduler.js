export default {
  async scheduled(controller, env, ctx) {
    const response = await fetch(
      "https://api.github.com/repos/BenjaSanchez/habitats/actions/workflows/collect-readings.yml/dispatches",
      {
        method: "POST",
        headers: {
          "Accept": "application/vnd.github+json",
          "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
          "X-GitHub-Api-Version": "2022-11-28",
          "Content-Type": "application/json",
          "User-Agent": "habitats-scheduler"
        },
        body: JSON.stringify({ ref: "main" })
      }
    );

    if (!response.ok) {
      throw new Error(
        `GitHub dispatch failed: ${response.status} ${await response.text()}`
      );
    }

    console.log("Dispatched collect-readings workflow");
  }
};
