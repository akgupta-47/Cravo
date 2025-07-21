package models

type PaymentProduct struct {
	Name       string   `json:"name"`
	UnitAmount int64  `json:"unit_amount"`
	Quantity   int64  `json:"quantity"`
}

type PaymentObjects struct {
	UserID       *string 		  `json:"user_id"`
	TaxAmount 	 int64  		  `json:"tax_amount"`
	Delivery   	 int64  		  `json:"delivery"`
	PlatformFee  int64  		  `json:"platform_fee"`
	Products     []PaymentProduct `json:"products"`
}

