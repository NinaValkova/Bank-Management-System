import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AppNavbar from "./components/AppNavbar";

import HomePage from "./pages/HomePage";
import UserAuthPage from "./pages/UserAuthPage";
import AdminAuthPage from "./pages/AdminAuthPage";
import AdminDashboardPage from "./pages/AdminDashboardPage";

import UserBankLayout from "./pages/UserBankLayout";
import UserMenuPage from "./pages/UserMenuPage";
import BalancePage from "./pages/BalancePage";
import TransferPage from "./pages/TransferPage";
import UserInfoPage from "./pages/UserInfoPage";
import UpdateUserPage from "./pages/UpdateUserPage";
import CashDepositPage from "./pages/CashDepositPage";
import CashWithdrawPage from "./pages/CashWithdrawPage";
import UserTransactionHistoryPage from "./pages/UserTransactionHistoryPage";
import HelpSupportPage from "./pages/HelpSupportPage";
import UserWelcomePage from "./pages/UserWelcomePage";


export default function App() {
  return (
    <AuthProvider>
      <AppNavbar />

      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route path="/user/login" element={<UserAuthPage mode="login" />} />
        <Route path="/user/register" element={<UserAuthPage mode="register" />} />

        <Route path="/admin/login" element={<AdminAuthPage />} />

        {/* USER */}
        <Route element={<ProtectedRoute requireAdmin={false} />}>
            <Route path="/app" element={<UserBankLayout />}>
            <Route index element={<UserWelcomePage />} />
            <Route index element={<UserMenuPage />} />
            <Route path="balance" element={<BalancePage />} />
            <Route path="transfer" element={<TransferPage />} />
            <Route path="me" element={<UserInfoPage />} />
            <Route path="update" element={<UpdateUserPage />} />
            <Route path="deposit" element={<CashDepositPage />} />
            <Route path="withdraw" element={<CashWithdrawPage />} />
            <Route path="transactions" element={<UserTransactionHistoryPage />} />
            <Route path="support" element={<HelpSupportPage />} />
          </Route>
        </Route>

        {/* ADMIN */}
        <Route element={<ProtectedRoute requireAdmin={true} />}>
          <Route path="/admin" element={<AdminDashboardPage />} />
        </Route>

        <Route path="*" element={<div className="container py-4">404</div>} />
      </Routes>
    </AuthProvider>
  );
}
