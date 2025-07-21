package controller

import (
	"log"
	"os"

	models "github.com/akgupta-47/go-service/model"
	"github.com/gofiber/fiber/v2"
	"github.com/stripe/stripe-go/v76"
	"github.com/stripe/stripe-go/v76/checkout/session"
)



func StripePaymentController(c *fiber.Ctx) error {
	stripe.Key = os.Getenv("STRIPE_SECRET_KEY")

	var payment models.PaymentObjects

	if err := c.BodyParser(&payment); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	var lineItems []*stripe.CheckoutSessionLineItemParams

	for _, p := range payment.Products {
		lineItem := &stripe.CheckoutSessionLineItemParams{
			PriceData: &stripe.CheckoutSessionLineItemPriceDataParams{
				Currency: stripe.String("inr"),
				ProductData: &stripe.CheckoutSessionLineItemPriceDataProductDataParams{
					Name: stripe.String(p.Name),
				},
				UnitAmount: stripe.Int64(p.UnitAmount),
			},
			Quantity: stripe.Int64(p.Quantity),
		}
		lineItems = append(lineItems, lineItem)
	}

	params := &stripe.CheckoutSessionParams{
		LineItems: lineItems,
		Mode: stripe.String(string(stripe.CheckoutSessionModePayment)),
		SuccessURL: stripe.String("https://example.com/success"),
		CancelURL:  stripe.String("https://example.com/cancel"),
	}

	params.AutomaticTax = &stripe.CheckoutSessionAutomaticTaxParams{
		Enabled: stripe.Bool(true),
	}	  

	params.ShippingOptions = []*stripe.CheckoutSessionShippingOptionParams{
		{
		  ShippingRateData: &stripe.CheckoutSessionShippingOptionShippingRateDataParams{
			DisplayName: stripe.String("Delivery"),
			FixedAmount: &stripe.CheckoutSessionShippingOptionShippingRateDataFixedAmountParams{
			  Amount:   stripe.Int64(payment.Delivery), // $5.00
			  Currency: stripe.String("usd"),
			},
			Type: stripe.String("fixed_amount"),
		  },
		},
	}

	params.PaymentIntentData = &stripe.CheckoutSessionPaymentIntentDataParams{
		ApplicationFeeAmount: stripe.Int64(payment.PlatformFee), // $3 platform fee
		TransferData: &stripe.CheckoutSessionPaymentIntentDataTransferDataParams{
		  Destination: stripe.String("acct_connected_id"),
		},
	}	  

	s, err := session.New(params)
	if err != nil {
		log.Printf("session.New: %v", err)
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"checkout_url": s.URL})
}