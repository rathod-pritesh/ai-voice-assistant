<script>
  import { onMount } from "svelte";
  import { ShieldCheck, ArrowRight, ArrowLeft } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";

  let otp = ["", "", "", "", "", ""];
  let email = "";
  let error = "";

  onMount(() => {
    if (typeof window !== "undefined") {
      email = sessionStorage.getItem("reset_email") || "";
    }
  });

  function handleOtpInput(e, index) {
    const val = e.target.value;
    if (val.length > 1) {
      otp[index] = val.slice(-1);
    }
    if (val && index < 5) {
      const nextInput = document.getElementById(`otp-${index + 1}`);
      if (nextInput) nextInput.focus();
    }
  }

  function handleKeyDown(e, index) {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      const prevInput = document.getElementById(`otp-${index - 1}`);
      if (prevInput) prevInput.focus();
    }
  }

  async function handleVerifyOtp() {
    error = "";
    const fullOtp = otp.join("");
    if (fullOtp.length < 6) {
      error = "Please enter all 6 digits of the OTP code.";
      toast.error(error);
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp: fullOtp }),
      });

      const data = await res.json();

      if (!res.ok) {
        error = data.detail || "Invalid OTP code";
        toast.error(error);
        return;
      }

      sessionStorage.setItem("reset_otp", fullOtp);
      toast.success("OTP Code Verified!");
      goto("/reset-password");
    } catch (e) {
      console.error("Verify OTP error", e);
      error = "Network error while verifying OTP.";
      toast.error(error);
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-4 relative z-10">
  <div class="w-full max-w-md bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-xl shadow-slate-200/50 space-y-8">
    
    <div class="text-center space-y-3">

      <h2 class="text-3xl font-extrabold text-[#1C1E1D] tracking-tight">
        Verify <span class="text-[#2F7A5F]">OTP</span>
      </h2>

      <p class="text-[#646B67] text-sm">
        Enter the 6-digit security code sent to <br />
        <span class="text-[#2F7A5F] font-semibold">{email || "your email"}</span>
      </p>
    </div>

    <div class="space-y-6">
      <div class="relative flex items-center">
        <KeyRound class="absolute left-4 w-5 h-5 text-[#646B67]" />
        <input
          type="text"
          maxlength="6"
          bind:value={otp}
          placeholder="••••••"
          class="w-full pl-12 pr-4 py-3.5 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] text-xl tracking-[0.4em] font-mono text-center outline-none transition"
        />
      </div>

      <button
        on:click={handleVerifyOTP}
        class="w-full py-3.5 px-4 rounded-2xl text-white font-semibold bg-[#2F7A5F] hover:bg-[#26664E] shadow-lg shadow-[#2F7A5F]/20 transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer group"
      >
        <span>Verify Security Code</span>
        <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </button>
    </div>
  </div>
</div>
