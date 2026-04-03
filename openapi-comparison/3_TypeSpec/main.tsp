import "@typespec/http";
import "@typespec/openapi3";
import "@typespec/rest";

using TypeSpec.Http;
using TypeSpec.OpenAPI;
using TypeSpec.Rest;

@service({
  title: "Library Management API",
  description: "API for managing library books",
  version: "1.0.0",
})
@server("http://localhost:5000", "Development server")
namespace LibraryApi;

@doc("Book information")
model Book {
  @doc("Unique book ID")
  id: int32;

  @doc("Book title")
  title: string;

  @doc("Book author")
  author: string;

  @doc("ISBN number")
  isbn: string;

  @doc("Publication year")
  @minValue(1000)
  @maxValue(2100)
  year?: int32;

  @doc("Whether the book is available")
  available?: boolean = true;
}

@doc("Request to create a new book")
model CreateBookRequest {
  @doc("Book title")
  title: string;

  @doc("Book author")
  author: string;

  @doc("ISBN number")
  isbn: string;

  @doc("Publication year")
  @minValue(1000)
  @maxValue(2100)
  year?: int32;

  @doc("Whether the book is available")
  available?: boolean = true;
}

@doc("Request to update a book")
model UpdateBookRequest {
  @doc("Book title")
  title?: string;

  @doc("Book author")
  author?: string;

  @doc("ISBN number")
  isbn?: string;

  @doc("Publication year")
  @minValue(1000)
  @maxValue(2100)
  year?: int32;

  @doc("Whether the book is available")
  available?: boolean;
}

@route("/books")
interface Books {
  @doc("Get all books")
  @get
  list(): Book[];

  @doc("Create a new book")
  @post
  create(@body book: CreateBookRequest): Book;

  @doc("Get a book by ID")
  @get
  @route("{id}")
  getById(@path id: int32): Book;

  @doc("Update a book")
  @put
  @route("{id}")
  update(@path id: int32, @body book: UpdateBookRequest): Book;

  @doc("Delete a book")
  @delete
  @route("{id}")
  delete(@path id: int32): void;
}
