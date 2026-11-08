import { describe, expect, it } from "vitest";
import { APP_NAME, APP_TAGLINE, APP_VERSION } from "./app-info";

describe("app info", () => {
  it("ha un nome e una tagline non vuoti", () => {
    expect(APP_NAME).toBe("Ripeti");
    expect(APP_TAGLINE.length).toBeGreaterThan(0);
  });

  it("espone una versione in formato semver", () => {
    expect(APP_VERSION).toMatch(/^\d+\.\d+\.\d+$/);
  });
});
