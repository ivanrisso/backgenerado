# DOMAIN RULES — BILLING & ACCOUNTING

## 0. Purpose
This document defines the business and accounting rules for the Billing domain.
It complements SYSTEM_FOUNDATION.md and MUST be followed by backend and frontend implementations.

---

## 1. Core Principle

CRUD operations are allowed ONLY for:
- Master Entities
- Subordinate entities (1 → N) without accounting impact

Accounting documents are immutable domain events.

---

## 2. Entity Classification

### 2.1 Master Entities (CRUD allowed)
- Customer
- Product / Service
- PriceList
- TaxProfile
- Currency
- PaymentMethod
- CompanySettings
- Branch / PointOfSale

### 2.2 Subordinate Entities (CRUD allowed if 1 → N)
- CustomerAddress
- CustomerContact
- CustomerBankAccount
- ProductPrice
- ProductTax

Rules:
- They cannot exist without their parent
- They do not generate accounting movements
- Changes affect only future operations

---

## 3. Accounting Documents (NO CRUD)

### 3.1 Immutable Events
- Invoice
- CreditNote
- DebitNote
- Payment
- PaymentAllocation

Rules:
- Once issued, they cannot be edited or deleted
- They are append-only
- Corrections are done through new documents

---

## 4. Invoice Lifecycle

### 4.1 Allowed Operations
- Issue
- Read
- Cancel (with rules)
- Correct via Credit/Debit Note
- Affect via Payment Allocation

### 4.2 Forbidden Operations
- Edit totals, items, customer, dates
- Delete invoice

### 4.3 States
- Draft
- Issued
- PartiallyPaid
- Paid
- Cancelled

---

## 5. Credit / Debit Notes

- Must reference original invoice
- Credit Note reduces balance
- Debit Note increases balance
- Used for corrections only

---

## 6. Payments & Allocation

### 6.1 Payment
- Independent entity
- Does not modify invoice directly

### 6.2 Allocation
- N ↔ N relationship
- Entity: PaymentAllocation
- Fields:
  - payment_id
  - invoice_id
  - amount
  - date

### 6.3 Derived States
- Invoice:
  - Pending (balance = total)
  - Partial (0 < balance < total)
  - Paid (balance = 0)
- Payment:
  - Available
  - PartiallyAllocated
  - Allocated

---

## 7. Invariants
- Invoice balance can never be negative
- Allocated amount cannot exceed payment amount
- Allocated amount cannot exceed invoice balance
- All accounting changes are traceable

---

## 8. Auditability
- All documents store:
  - created_by
  - created_at
  - reason (for cancellation)
- No hard deletes allowed
