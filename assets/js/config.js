/* Nirog.com site configuration.
   Payments: paste a UPI ID, PayPal donate link, Stripe Payment Link, Razorpay page or Buy Me a Coffee URL
   to switch the Support page from "pledge" mode to instant checkout. Leave blank to keep pledge mode. */
window.SITE = {
  name: "Nirog.com",
  domain: "nirog.com",
  ownerContactUrl: "https://web.works/contact",
  adsenseClient: "ca-pub-6620975821265271",
  payments: {
    upi: "",           // e.g. yourname@okbank  (shows a "Pay by UPI" button + deep link)
    razorpay: "",      // e.g. https://rzp.io/l/XXXX
    paypal: "",        // e.g. https://www.paypal.com/donate/?hosted_button_id=XXXX
    stripe: "",        // e.g. https://buy.stripe.com/XXXX
    buymeacoffee: ""   // e.g. https://www.buymeacoffee.com/yourname
  },
  /* Form relay key (encoded). Keep it encoded: never paste a plain address anywhere on the site. */
  _k: ["MWFza3Jvd2Jldw==", "bW9jLmxpYW1n"]
};
