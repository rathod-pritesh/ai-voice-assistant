<script>
  import { Mail, ArrowLeft, ArrowRight } from "lucide-svelte";
  import { goto } from '$app/navigation';
  import { toast } from 'svelte-sonner';

  let email = "";
  let error = "";

  async function handleForgotPassword() {
    error = "";
    if (!email.trim()) {
      error = "Email address is required.";
      toast.error(error);
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() })
      });

      const data = await res.json();

      if (!res.ok) {
        error = data.detail || "Failed to send reset OTP.";
        toast.error(error);
        return;
      }

      sessionStorage.setItem("reset_email", email.trim());
      toast.success("Verification OTP code sent to your email!");
      goto("/verify-otp");

    } catch (err) {
      console.error("Forgot password error", err);
      error = "Network error while connecting to server.";
      toast.error(error);
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-4 relative z-10">
  <div class="w-full max-w-md bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-xl shadow-slate-200/50 space-y-8">
    
    <div class="text-center space-y-3">
      <h2 class="text-3xl font-extrabold text-[#1C1E1D] tracking-tight">
        Forgot <span class="text-[#2F7A5F]">Password?</span>
      </h2>
      <p class="text-[#646B67] text-sm">
        Enter your email address to receive your 6-digit verification code
      </p>
    </div>

    <form on:submit|preventDefault={handleForgotPassword} class="space-y-6">
      <div class="space-y-1.5">
        <label for="email" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Email Address
        </label>
        <div class="relative flex items-center">
          <Mail class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type="email"
            id="email"
            bind:value={email}
            required
            class="w-full pl-12 pr-4 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="you@example.com"
          />
        </div>
      </div>

      <button
        type="submit"
        class="w-full py-3.5 px-4 rounded-2xl text-white font-semibold bg-[#2F7A5F] hover:bg-[#26664E] shadow-lg shadow-[#2F7A5F]/20 transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer group"
      >
        <span>Send Verification Code</span>
        <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </button>

      <div class="text-center pt-2">
        <a href="/login" class="inline-flex items-center gap-2 text-xs text-[#646B67] hover:text-[#1C1E1D] transition">
          <ArrowLeft class="w-3.5 h-3.5" />
          Back to Login
        </a>
      </div>
    </form>
  </div>
</div>
