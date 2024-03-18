import React from "react";

export default function Header() {
  return (
    <div className="header">
        <div className="header_left">
            <img
              src="images/ucscLogo_white.jpg" // Replace with the URL of your logo image
              alt=""
              className="header_logo"
            />
        </div>
        <div className="header_center">
          <span>TA BOT for SE-UCSC</span>
        </div>
    </div>
  );
}
