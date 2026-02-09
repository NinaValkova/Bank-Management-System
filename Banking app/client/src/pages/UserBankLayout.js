import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function UserBankLayout() {
  const auth = useAuth();
  const navigate = useNavigate();

  const logout = () => {
    auth.clearToken();
    navigate("/user/login");
  };

  return (
    <div className="bank-shell">

      <div className="bank-layout">
        {/* LEFT MENU */}
        <div className="bank-side">
          <NavLink className="bank-btn" to="/app/balance">BALANCE INQUIRY</NavLink>
          <NavLink className="bank-btn" to="/app/transfer">TRANSFER</NavLink>
          <NavLink className="bank-btn" to="/app/me">USER INFORMATION</NavLink>
          <NavLink className="bank-btn" to="/app/update">UPDATE DETAILS</NavLink>
        </div>

        {/* CENTER */}
        <div className="bank-center">
          <Outlet />
        </div>

        {/* RIGHT MENU (disabled buttons like screenshot) */}
        <div className="bank-side">
          <NavLink className="bank-btn" to="/app/deposit">CASH DEPOSIT</NavLink>
          <NavLink className="bank-btn" to="/app/withdraw">CASH WITHDRAWAL</NavLink>
          <NavLink className="bank-btn" to="/app/transactions">TRANSACTION HISTORY</NavLink>
          <NavLink className="bank-btn" to="/app/support">HELP SUPPORT</NavLink>
        </div>
      </div>
    </div>
  );
}
