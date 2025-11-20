<script>
  import { onMount } from "svelte";
  import { initHomeAnimation } from "$lib/animations/homeAnimation";
  import { goto } from "$app/navigation";

  let canvas;
  let email = "";
  let newPassword = "";
  let confirmPassword = "";

  onMount(() => {
    email = sessionStorage.getItem("reset_email");
    if (!email) window.location.href = "/forgot-password";

    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  });

  async function handleResetPassword() {
    if (!newPassword.trim() || !confirmPassword.trim()) {
      alert("Please enter all fields");
      return;
    }

    if (newPassword !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const res = await fetch("http://localhost:8000/api/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, new_password: newPassword })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);
      return;
    }

    alert("Password reset successfully!");
    sessionStorage.removeItem("reset_email");

    goto("/login")
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-black p-4 relative">
  <canvas bind:this={canvas} class="fixed inset-0 w-full h-full pointer-events-none"></canvas>

  <div class="w-full max-w-md bg-slate-900/80 backdrop-blur-xl border border-slate-700 p-8 rounded-2xl shadow-2xl">
    <h2 class="text-3xl font-bold text-center text-white mb-6">
      Reset Password
    </h2>

    <div class="space-y-6">
      <input
        type="password"
        bind:value={newPassword}
        placeholder="Enter new password"
        class="w-full px-4 py-3 rounded-lg bg-black/40 border border-slate-600 text-white text-lg focus:ring-cyan-500"
      />

      <input
        type="password"
        bind:value={confirmPassword}
        placeholder="Confirm new password"
        class="w-full px-4 py-3 rounded-lg bg-black/40 border border-slate-600 text-white text-lg focus:ring-cyan-500"
      />

      <button
        on:click={handleResetPassword}
        class="w-full py-3 text-lg rounded-lg bg-gradient-to-r from-green-600 to-emerald-700 hover:from-green-500 hover:to-emerald-600 text-white shadow-lg transition"
      >
        Save New Password
      </button>
    </div>
  </div>
</div>
