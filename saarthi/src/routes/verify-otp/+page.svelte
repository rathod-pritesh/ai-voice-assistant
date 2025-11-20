<script>
  import { onMount } from "svelte";
  import { initHomeAnimation } from "$lib/animations/homeAnimation";

  let canvas;
  let otp = "";
  let email = "";

  onMount(() => {
    email = sessionStorage.getItem("reset_email");
    if (!email) window.location.href = "/forgot-password";

    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  });

  async function handleVerifyOTP() {
    if (!otp.trim() || otp.length !== 6) {
      alert("Enter a valid 6-digit OTP");
      return;
    }

    const res = await fetch("http://localhost:8000/api/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);
      return;
    }

    alert("OTP Verified");
    window.location.href = "/reset-password";
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-black p-4 relative">
  <canvas bind:this={canvas} class="fixed inset-0 w-full h-full pointer-events-none"></canvas>

  <div class="w-full max-w-md bg-slate-900/80 backdrop-blur-xl border border-slate-700 p-8 rounded-2xl shadow-2xl">
    <h2 class="text-3xl font-bold text-center text-white mb-8">
      Verify OTP
    </h2>

    <p class="text-center text-gray-300 mb-6">
      OTP sent to <span class="text-cyan-400 font-semibold">{email}</span>
    </p>

    <div class="space-y-6">
      <input
        type="text"
        maxlength="6"
        bind:value={otp}
        placeholder="Enter 6-digit OTP"
        class="w-full px-4 py-3 rounded-lg bg-black/40 border border-slate-600 text-white text-lg tracking-widest text-center focus:ring-cyan-500"
      />

      <button
        on:click={handleVerifyOTP}
        class="w-full py-3 text-lg rounded-lg bg-gradient-to-r from-cyan-600 to-blue-700 hover:from-cyan-500 hover:to-blue-600 text-white shadow-lg transition"
      >
        Verify OTP
      </button>
    </div>
  </div>
</div>
