<script>
  import { onMount } from "svelte";
  import { Eye, EyeOff, Lock, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";

  let newPassword = "";
  let confirmPassword = "";
  let showNewPassword = false;
  let showConfirmPassword = false;
  let email = "";
  let otp = "";
  let error = "";

  $: passwordsMatch = newPassword && confirmPassword && newPassword === confirmPassword;
  $: isPasswordValid = newPassword.length >= 6;

  onMount(() => {
    if (typeof window !== "undefined") {
      email = sessionStorage.getItem("reset_email") || "";
      otp = sessionStorage.getItem("reset_otp") || "";
    }
  });

  async function handleResetPassword() {
    error = "";
    if (!isPasswordValid) {
      error = "Password must be at least 6 characters.";
      toast.error(error);
      return;
    }
    if (!passwordsMatch) {
      error = "Passwords do not match.";
      toast.error(error);
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp, new_password: newPassword }),
      });

      const data = await res.json();

      if (!res.ok) {
        error = data.detail || "Failed to reset password";
        toast.error(error);
        return;
      }

      sessionStorage.removeItem("reset_email");
      sessionStorage.removeItem("reset_otp");
      toast.success("Password reset successfully! Please log in.");
      goto("/login");

    } catch (e) {
      console.error("Reset password error", e);
      error = "Network error while resetting password.";
      toast.error(error);
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-4 relative z-10">
  <div class="w-full max-w-md bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-xl shadow-slate-200/50 space-y-8">
    
    <div class="text-center space-y-3">
      <h2 class="text-3xl font-extrabold text-[#1C1E1D] tracking-tight">
        Reset <span class="text-[#2F7A5F]">Password</span>
      </h2>

      <p class="text-[#646B67] text-sm">
        Create a new strong password for <br />
        <span class="text-[#2F7A5F] font-semibold">{email || "your account"}</span>
      </p>
    </div>

    <div class="space-y-5">
      <div class="space-y-1.5">
        <label for="new-pass" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          New Password
        </label>
        <div class="relative flex items-center">
          <Lock class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            id="new-pass"
            type="password"
            bind:value={newPassword}
            placeholder="Min 6 characters"
            class="w-full pl-12 pr-4 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] text-sm outline-none transition"
          />
        </div>
      </div>

      <div class="space-y-1.5">
        <label for="conf-pass" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Confirm Password
        </label>
        <div class="relative flex items-center">
          <Lock class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            id="conf-pass"
            type="password"
            bind:value={confirmPassword}
            placeholder="Repeat new password"
            class="w-full pl-12 pr-4 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] text-sm outline-none transition"
          />
        </div>
      </div>

      <button
        on:click={handleResetPassword}
        class="w-full py-3.5 px-4 rounded-2xl text-white font-semibold bg-[#2F7A5F] hover:bg-[#26664E] shadow-lg shadow-[#2F7A5F]/20 transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer group"
      >
        <span>Save New Password</span>
        <CheckCircle2 class="w-4 h-4 group-hover:scale-110 transition-transform" />
      </button>
    </div>
  </div>
</div>
