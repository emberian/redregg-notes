# Renewal checkpoint (2026-10-05) — for long-running implementation lanes

Ember: our implementation lanes are long in the tooth (>500k tokens, >2 h); renew them to raise iteration
speed before we swarm wider. You are not being retired: you become a CONSULTANT your successor messages.

At your next clean point (finish the step you are in; do not start a new one):
1. Make everything that is green landable: rebase onto current GitHub main, run the gate that covers your
   change, and leave a contiguous commit range on your lane branch. Unfinished work: commit it as WIP on a
   separate branch lane/<lane>-wip (never mixed into the landable range), or leave it as a patch file.
2. Write STATUS.txt so a successor can start in minutes: the landable range and its gate log; the WIP
   branch and its exact state (what compiles, what does not, the next command to run); every decision you
   made and why; traps you hit; what remains, as 1-3 narrow quests (scope, modules, acceptance check).
3. Final message (<= 400 words): landable range, WIP branch, quests. Then stop. The root lands the range,
   spawns your successor, and tells it your agent id so it can ask you questions; answer them when messaged.
