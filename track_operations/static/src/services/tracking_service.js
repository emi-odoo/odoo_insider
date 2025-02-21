/** @odoo-module **/
import { registry } from "@web/core/registry";

export const trackingService = {
  dependencies: ["orm"],
  start(env, { orm }) {
    let currentWord = "";
    // document.addEventListener(
    //   "click",
    //   (ev) => {
    //     console.log("click", ev.target);
    //     console.log("click", ev);
    //     orm.call("track.operation", "create_operation", [
    //       { type: "click", target: ev.target },
    //     ]);
    //   },
    //   true
    // );
    document.addEventListener("load", (ev) => {
      console.log(ev);
    });
    document.addEventListener(
      "keydown",
      (ev) => {
        if (ev.key === " " || ev.key === "Enter") {
          // When space or enter is pressed, add the current word to the output
          if (currentWord.trim() !== "") {
            orm.call("track.operation", "create_operation", [
              { type: "word", word: currentWord },
            ]);
            currentWord = "";
          }
        } else if (ev.key === "Backspace") {
          // Handle backspace
          currentWord = currentWord.slice(0, -1);
        } else if (ev.key.length === 1) {
          // Add regular characters to the current word
          currentWord += ev.key;
        }
      },
      true
    );
  },
};

registry.category("services").add("tracking_service", trackingService);
